import numpy as np
import pytest
from packages.pipeline.pipeline import run_full_pipeline
from schema.models import ScenePlan

def test_pipeline_cluttered_scene_rejection():
    # 1. Load mock data
    data = np.load("ml/demo_scenes/demo_cluttered.npz", allow_pickle=True)
    depth = data["depth"]
    
    payload = {
        "job_id": "test_job_123",
        "scene_id": "scene_cluttered_01",
        "depth": depth,
        "jaw_width_mm": float(data["jaw_width_mm"]),
        "max_aperture_mm": float(data["max_aperture_mm"]),
        # We inject force_failure to guarantee O-score > threshold logic hits in the mock
        "force_failure": True
    }
    
    # 2. Run mock pipelined logic
    result = run_full_pipeline(payload, device="cpu")
    
    # Validation
    parsed_plan = ScenePlan(**result)
    
    # 3. Assert ALL scores are in [0, 1]
    for g in parsed_plan.top_10_grasps:
        assert 0.0 <= g.audit.s_score <= 1.0
        assert 0.0 <= g.audit.c_score <= 1.0
        assert 0.0 <= g.audit.o_score <= 1.0
        assert 0.0 <= g.audit.r_score <= 1.0
        assert 0.0 <= g.audit.k_score <= 1.0
        assert 0.0 <= g.audit.tci_score <= 1.0
        assert 0.0 <= g.audit.gtv_score <= 1.0
        assert 0.0 <= g.audit.g_safe <= 1.0
        
    # 4. Assert at least one grasp in top-10 is rejected
    rejections = [g for g in parsed_plan.top_10_grasps if g.rejected]
    assert len(rejections) > 0, "No grasps were rejected, but at least one should have failed the O-score threshold."
    
    # Verify O-score failure logic specifically for the first one since we targeted it 
    assert rejections[0].audit.o_score > 0.55
    assert "High Uncertainty" in rejections[0].audit.flags
