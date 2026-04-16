import numpy as np
from datetime import datetime, timezone
import json

from packages.schema.models import ScenePlan, GraspOutput, GraspPose, AuditScores, BenchmarkReference
from .helpers import (
    emit_progress, get_nearest_normal, compute_gripper_aabb,
    count_points_in_box, count_points_near_ray_kdtree,
    spatial_nms, project_masks_to_pointcloud, compute_tci_per_grasp,
    simulate_grasp_pybullet
)

def run_full_pipeline(payload: dict, device: str) -> dict:
    job_id = payload.get("job_id", "local_test_id")
    scene_id = payload.get("scene_id", "dummy_scene")
    
    # STEP 1: Load payload
    depth = payload.get("depth") # np array
    jaw_width_mm = payload.get("jaw_width_mm", 85.0)
    max_aperture_mm = payload.get("max_aperture_mm", 80.0)
    
    emit_progress(job_id, "depth_repair", 5)

    # STEP 2: Depth repair (mocked)
    emit_progress(job_id, "pointcloud", 10)
    
    # STEP 3: Point Cloud (mocked to N points)
    # create synthetic pointcloud centered at origin for testing
    num_points = 1000
    pcd_points = np.random.randn(num_points, 3) * 0.5 
    pcd_normals = np.zeros_like(pcd_points)
    pcd_normals[:, 2] = 1.0 # pointing up
    
    emit_progress(job_id, "segmentation", 18)
    # STEP 4: SAM2 Segmentation
    
    emit_progress(job_id, "grasp_generation", 30)
    # STEP 5: Contact-GraspNet Predict To-50 Grasps
    num_grasps = 15
    candidates = []
    
    # Intentionally trigger an uncertainty variance issue if 'force_failure' is in payload
    force_failure = payload.get("force_failure", False)
    
    for i in range(num_grasps):
        pose = np.eye(4)
        pose[:3, 3] = np.random.randn(3) * 0.2
        confidence = np.random.rand()
        candidates.append({"id": f"g_{i}", "pose": pose, "score": confidence})

    emit_progress(job_id, "audit", 45)
    
    # STEP 6: Failure mode audit & STEP 7: Novel Modules
    scored_grasps = []
    
    for idx, c in enumerate(candidates):
        pose = c["pose"]
        pos = pose[:3, 3]
        
        # TYPE-S: Approach angle vs surface normal
        angle_rad = np.random.rand() * np.pi/4
        s_score = np.clip(1.0 - abs(np.cos(angle_rad)), 0.0, 1.0)
        
        # TYPE-C: Collision points in AABB
        aabb = compute_gripper_aabb(pose, jaw_width_mm, max_aperture_mm)
        pts_inside = count_points_in_box(pcd_points, aabb)
        c_score = np.clip(pts_inside / 50.0, 0.0, 1.0)
        
        # TYPE-O: Depth uncertainty
        if force_failure and idx == 0:
            std = 0.06 # Will force o_score = min(1, 0.06/0.05) = 1.0
        else:
            std = np.random.rand() * 0.02
        o_score = np.clip(std / 0.05, 0.0, 1.0)
        
        # TYPE-R: Retraction
        blocked = np.random.randint(0, 10)
        r_score = np.clip(blocked / 20.0, 0.0, 1.0)
        
        # TYPE-K: Cascade
        k_score = np.clip(np.random.rand() * 0.4, 0.0, 1.0)
        
        # STEP 7: GTV, TCI, Reachability
        gtv_score = np.clip(np.random.rand(), 0.0, 1.0)
        tci_score = np.clip(np.random.rand(), 0.0, 1.0)
        reach = True
        
        # STEP 8: G-SAFE composite
        g_safe = ((1-s_score) + (1-c_score) + (1-o_score) + (1-r_score) + (1-k_score) + (1-tci_score) + gtv_score + c["score"]) / 8.0
        if not reach:
            g_safe *= 0.5
            
        c["audit"] = {
            "s_score": s_score, "c_score": c_score, "o_score": o_score,
            "r_score": r_score, "k_score": k_score, "tci_score": tci_score,
            "gtv_score": gtv_score, "g_safe": g_safe, "reach": reach
        }
        scored_grasps.append(c)

    emit_progress(job_id, "novel_modules", 60)
    
    # NMS
    nms_grasps = spatial_nms(scored_grasps, pos_thresh=0.015, angle_thresh=0.26)
    # top 10
    top_10 = nms_grasps[:10]
    
    emit_progress(job_id, "agents", 80)
    
    # STEP 9: Self-rejection gate
    final_outputs = []
    has_rank_1_rejected = False
    first_operational = False
    
    for i, g in enumerate(top_10):
        a = g["audit"]
        flags = []
        rejected = False
        reason = None
        
        if a["s_score"] > 0.60: flags.append("High Slip Risk"); rejected = True; reason="S-Score exceeded"
        if a["c_score"] > 0.50: flags.append("Collision Risk"); rejected = True; reason="C-Score exceeded"
        if a["o_score"] > 0.55: flags.append("High Uncertainty"); rejected = True; reason="O-Score exceeded"
        if a["r_score"] > 0.60: flags.append("Retraction Blocked"); rejected = True; reason="R-Score exceeded"
        if a["k_score"] > 0.50: flags.append("Cascade Risk"); rejected = True; reason="K-Score exceeded"
        
        if i == 0 and rejected:
            has_rank_1_rejected = True
            
        is_operational = False
        if not rejected and not first_operational:
            is_operational = True
            first_operational = True
            
        # STEP 10: PyBullet simulation for top-3
        sim_validated = None
        if i < 3:
            # mock physics_client for test
            sim_validated = simulate_grasp_pybullet(g, scene_id, physics_client=None)

        final_outputs.append({
            "grasp": {
                "grasp_id": g["id"],
                "position": {"x": float(g["pose"][0,3]), "y": float(g["pose"][1,3]), "z": float(g["pose"][2,3])},
                "orientation": {"x": 0.0, "y": 0.0, "z": 0.0, "w": 1.0},
                "pre_grasp_approach": {"x": 0, "y": 0, "z": -1},
                "post_grasp_retreat": {"x": 0, "y": 0, "z": 1},
                "grasp_quality": float(g["audit"]["g_safe"]),
                "max_contact_force": 0.0
            },
            "audit": {
                "s_score": float(a["s_score"]), "c_score": float(a["c_score"]), "o_score": float(a["o_score"]),
                "r_score": float(a["r_score"]), "k_score": float(a["k_score"]), "tci_score": float(a["tci_score"]),
                "gtv_score": float(a["gtv_score"]), "g_safe": float(a["g_safe"]), "reach": a["reach"],
                "flags": flags, "rejection_reason": reason, "explanation": ""
            },
            "rank": i + 1,
            "rejected": rejected,
            "is_rank1_override": (has_rank_1_rejected and is_operational),
            "is_operational": is_operational,
            "sim_validated": sim_validated
        })

    emit_progress(job_id, "complete", 100)

    # Validate against Schema
    plan = ScenePlan(
        scene_id=scene_id,
        job_id=job_id,
        timestamp=datetime.now(timezone.utc).isoformat(),
        inference_time_seconds=2.45,
        collision_free_ratio=1.0 - (sum(1 for g in final_outputs if g["audit"]["c_score"]>0.5)/max(1, len(final_outputs))),
        collision_free_count=sum(1 for g in final_outputs if g["audit"]["c_score"]<=0.5),
        object_count=3,
        benchmark=BenchmarkReference(),
        top_10_grasps=[GraspOutput(**x) for x in final_outputs],
        agents_resolved=False
    )
    
    return plan.model_dump()
