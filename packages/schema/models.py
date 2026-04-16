"""
GRASP Platform — Pydantic v2 Schema Models
packages/schema/models.py
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class GraspPose(BaseModel):
    grasp_id: str
    position: dict        # {x, y, z} metres
    orientation: dict     # {x, y, z, w} quaternion
    pre_grasp_approach: dict
    post_grasp_retreat: dict
    grasp_quality: float  # = g_safe score, 0-1
    max_contact_force: float = 0.0


class AuditScores(BaseModel):
    s_score: float = Field(ge=0.0, le=1.0)
    c_score: float = Field(ge=0.0, le=1.0)
    o_score: float = Field(ge=0.0, le=1.0)
    r_score: float = Field(ge=0.0, le=1.0)
    k_score: float = Field(ge=0.0, le=1.0)
    tci_score: float = Field(ge=0.0, le=1.0)
    gtv_score: float = Field(ge=0.0, le=1.0)
    g_safe: float = Field(ge=0.0, le=1.0)
    reach: bool
    flags: List[str]
    rejection_reason: Optional[str] = None
    explanation: str = ""


class GraspOutput(BaseModel):
    grasp: GraspPose
    audit: AuditScores
    rank: int
    rejected: bool
    is_rank1_override: bool = False
    is_operational: bool = False
    sim_validated: Optional[bool] = None


class BenchmarkReference(BaseModel):
    seen_split_ap: float = 73.6
    unseen_split_ap: float = 63.4
    method: str = "Contact-GraspNet + Spatial NMS + G-SAFE Reranking"
    evaluation_date: str = "2026-04"


class ScenePlan(BaseModel):
    scene_id: str
    job_id: str
    timestamp: str
    scene_summary: str = ""
    inference_time_seconds: float
    collision_free_ratio: float
    collision_free_count: int
    object_count: int
    benchmark: BenchmarkReference
    top_10_grasps: List[GraspOutput]
    agents_resolved: bool = False
