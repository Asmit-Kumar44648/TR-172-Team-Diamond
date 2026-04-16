// GRASP Platform Frontend Data Models (Strict Sync with packages/schema/models.py)

export interface Vector3D {
  x: number;
  y: number;
  z: number;
  w?: number;
}

export interface GraspPose {
  grasp_id: string;
  position: Vector3D;
  orientation: Vector3D;
  pre_grasp_approach: Vector3D;
  post_grasp_retreat: Vector3D;
  grasp_quality: number;
  max_contact_force: number;
}

export interface AuditReasoning {
  s_score: number;
  c_score: number;
  o_score: number;
  r_score: number;
  k_score: number;
  tci_score: number;
  gtv_score: number;
  g_safe: number;
  reach: boolean;
  flags: string[];
  rejection_reason: string | null;
  explanation: string;
}

export interface GraspRecord {
  grasp: GraspPose;
  audit: AuditReasoning;
  rank: number;
  rejected: boolean;
  is_rank1_override: boolean;
  is_operational: boolean;
  sim_validated: boolean | null;
}

export interface BenchmarkStats {
  seen_split_ap?: number;
  unseen_split_ap?: number;
  method?: string;
  evaluation_date?: string;
}

export interface ScenePlan {
  scene_id: string;
  job_id: string;
  timestamp: string;
  scene_summary?: string;
  inference_time_seconds: number;
  collision_free_ratio: number;
  collision_free_count: number;
  object_count: number;
  top_10_grasps: GraspRecord[];
  agents_resolved: boolean;
  benchmark: BenchmarkStats;
}

// Demo SSE Messages
export interface StreamMessage {
  type: 'connected' | 'progress' | 'complete' | 'agent_start' | 'scene_summary' | 'explanations' | 'reranking' | 'agents_complete' | 'error';
  job_id?: string;
  stage?: string;
  progress?: number;
  result?: ScenePlan;
  content?: any;
  message?: string;
}
