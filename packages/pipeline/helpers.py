import numpy as np
import os
import json

def emit_progress(job_id: str, stage: str, pct: int) -> None:
    # If redis was directly available, we'd use it:
    # redis.set(f"progress:{job_id}", json.dumps({"stage": stage, "progress": pct}))
    # For now, print for logging
    print(f"[{job_id}] Stage: {stage} -> {pct}%")

def get_nearest_normal(contact_pt, pcd_points, pcd_normals) -> np.ndarray:
    dists = np.linalg.norm(pcd_points - contact_pt, axis=1)
    idx = np.argmin(dists)
    return pcd_normals[idx]

def compute_gripper_aabb(pose_4x4, jaw_width, max_aperture) -> dict:
    position = pose_4x4[:3, 3]
    # Simple analytical AABB relative to world
    half_w = jaw_width / 2.0 / 1000.0
    half_a = max_aperture / 2.0 / 1000.0
    # Overly simplified analytical AABB for mock purposes
    return {
        "min_x": position[0] - half_w, "max_x": position[0] + half_w,
        "min_y": position[1] - half_a, "max_y": position[1] + half_a,
        "min_z": position[2] - 0.05,  "max_z": position[2] + 0.05
    }

def count_points_in_box(points, aabb) -> int:
    mask_x = (points[:, 0] >= aabb["min_x"]) & (points[:, 0] <= aabb["max_x"])
    mask_y = (points[:, 1] >= aabb["min_y"]) & (points[:, 1] <= aabb["max_y"])
    mask_z = (points[:, 2] >= aabb["min_z"]) & (points[:, 2] <= aabb["max_z"])
    return np.sum(mask_x & mask_y & mask_z)

def count_points_near_ray_kdtree(origin, end, kdtree, radius, n_samples) -> int:
    return np.random.randint(0, 5) # Mock implementation

def spatial_nms(candidates, pos_thresh, angle_thresh) -> list:
    # Candidates has form: [{"id": x, "pose": pose, "score": s}]
    # Sort by score desc
    candidates = sorted(candidates, key=lambda x: x["score"], reverse=True)
    kept = []
    
    for c in candidates:
        pos_c = c["pose"][:3, 3]
        duplicate = False
        for k in kept:
            pos_k = k["pose"][:3, 3]
            dist = np.linalg.norm(pos_c - pos_k)
            # Assuming perfectly parallel angle mock for now
            if dist < pos_thresh:
                duplicate = True
                break
        if not duplicate:
            kept.append(c)
    return kept

def project_masks_to_pointcloud(masks, pcd_points, intrinsics, depth) -> dict:
    # dict[int, np.ndarray] mapping mask ID to pointcloud subset
    return {0: pcd_points} # Mock

def pointcloud_to_voxel_grid(points, voxel_size) -> np.ndarray:
    return np.zeros((10,10,10), dtype=bool)

def create_sphere_kernel(radius_v) -> np.ndarray:
    dim = 2 * radius_v + 1
    kernel = np.zeros((dim, dim, dim), dtype=bool)
    # create sphere shape mock
    kernel[radius_v, radius_v, radius_v] = True 
    return kernel

def world_to_voxel(point, origin, voxel_size) -> tuple:
    return (0, 0, 0)

def compute_tci_per_grasp(grasps, pts_tda, diagrams) -> np.ndarray:
    return np.random.rand(len(grasps))

def simulate_grasp_pybullet(grasp, scene_id, physics_client) -> bool:
    return True
