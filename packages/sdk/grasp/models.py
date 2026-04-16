from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import json

@dataclass
class Vector3:
    x: float
    y: float
    z: float
    w: Optional[float] = None

@dataclass
class GraspPose:
    grasp_id: str
    position: Dict[str, float]
    orientation: Dict[str, float]
    pre_grasp_approach: Dict[str, float]
    post_grasp_retreat: Dict[str, float]
    grasp_quality: float
    max_contact_force: float

@dataclass
class AuditScores:
    s_score: float
    c_score: float
    o_score: float
    r_score: float
    k_score: float
    tci_score: float
    gtv_score: float
    g_safe: float
    reach: bool
    flags: List[str]
    rejection_reason: Optional[str]
    explanation: str

@dataclass
class GraspOutput:
    grasp: GraspPose
    audit: AuditScores
    rank: int
    rejected: bool
    is_rank1_override: bool
    is_operational: bool
    sim_validated: Optional[bool] = None

@dataclass
class ScenePlan:
    scene_id: str
    job_id: str
    timestamp: str
    inference_time_seconds: float
    collision_free_ratio: float
    collision_free_count: int
    object_count: int
    top_10_grasps: List[GraspOutput]
    scene_summary: str = ""

    def to_ros_json(self, file_path: str):
        """Exports the top-ranked grasp plan to a ROS MoveIt compatible JSON file."""
        # This will be implemented in ros.py or directly here.
        # For simplicity in the SDK, we'll put the primary logic here.
        plan_data = {
            "scene_id": self.scene_id,
            "job_id": self.job_id,
            "timestamp": self.timestamp,
            "grasps": [
                {
                    "rank": g.rank,
                    "rejected": g.rejected,
                    "operational": g.is_operational,
                    "pose": {
                        "position": g.grasp.position,
                        "orientation": g.grasp.orientation
                    },
                    "approach": g.grasp.pre_grasp_approach,
                    "retreat": g.grasp.post_grasp_retreat
                } for g in self.top_10_grasps
            ]
        }
        with open(file_path, 'w') as f:
            json.dump(plan_data, f, indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ScenePlan':
        """Constructs a ScenePlan object from the API JSON response."""
        grasps = []
        for g in data.get("top_10_grasps", []):
            pose_data = g["grasp"]
            audit_data = g["audit"]
            
            pose = GraspPose(**pose_data)
            audit = AuditScores(**audit_data)
            
            grasps.append(GraspOutput(
                grasp=pose,
                audit=audit,
                rank=g["rank"],
                rejected=g["rejected"],
                is_rank1_override=g.get("is_rank1_override", False),
                is_operational=g.get("is_operational", False),
                sim_validated=g.get("sim_validated")
            ))
            
        return cls(
            scene_id=data["scene_id"],
            job_id=data["job_id"],
            timestamp=data["timestamp"],
            inference_time_seconds=data["inference_time_seconds"],
            collision_free_ratio=data["collision_free_ratio"],
            collision_free_count=data["collision_free_count"],
            object_count=data["object_count"],
            top_10_grasps=grasps,
            scene_summary=data.get("scene_summary", "")
        )

@dataclass
class UsageStats:
    used_today: int
    quota: int
    plan: str
    reset_at: str
