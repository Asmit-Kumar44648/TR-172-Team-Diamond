import httpx
import os
import numpy as np
import io
import time

# Configuration from env or defaults for local testing
API_URL = os.getenv("TEST_API_URL", "http://127.0.0.1:8000")
API_KEY = os.getenv("TEST_API_KEY", "grsp_live_demo_key_123")

def test_health():
    print(f"Testing health check at {API_URL}/health...")
    r = httpx.get(f"{API_URL}/health")
    assert r.status_code == 200
    print("✓ Health OK")

def test_upload_and_analyze():
    print("Testing full analysis flow...")
    
    # 1. Create minimal valid depth array (pseudo-cluttered scene)
    depth = np.random.uniform(0.5, 1.5, (480, 640)).astype(np.float32)
    buf = io.BytesIO()
    np.save(buf, depth)
    buf.seek(0)
    
    # 2. Upload scene
    print("Uploading depth scene...")
    r = httpx.post(
        f"{API_URL}/v1/scenes/upload",
        headers={"X-API-Key": API_KEY},
        files={"depth": ("test.npy", buf)},
        data={"jaw_width_mm": "85", "max_aperture_mm": "80"}
    )
    if r.status_code != 200:
        print(f"Upload failed: {r.text}")
    assert r.status_code == 200
    scene_id = r.json()["scene_id"]
    print(f"✓ Scene Uploaded: {scene_id}")
    
    # 3. Start analysis
    print("Triggering G-SAFE analysis...")
    r = httpx.post(
        f"{API_URL}/v1/analysis/run",
        headers={"X-API-Key": API_KEY},
        json={"scene_id": scene_id, "config": {}}
    )
    assert r.status_code == 200
    job_id = r.json()["job_id"]
    print(f"✓ Analysis Started: {job_id}")
    
    # 4. Poll for result (60s timeout for demo)
    print("Polling for results (timeout 60s)...")
    for i in range(120):
        time.sleep(0.5)
        r = httpx.get(
            f"{API_URL}/v1/analysis/{job_id}", # Polling the status endpoint we added in Phase 6
            headers={"X-API-Key": API_KEY}
        )
        if r.status_code == 200:
            data = r.json()
            if data.get("status") == "complete":
                result = data["result"]
                assert "top_10_grasps" in result
                assert len(result["top_10_grasps"]) <= 10
                
                # Verify scores are within range
                for g in result["top_10_grasps"]:
                    assert 0.0 <= g["audit"]["g_safe"] <= 1.0
                    
                print(f"✓ Smoke test passed: {len(result['top_10_grasps'])} grasps audited.")
                return
            elif data.get("status") == "failed":
                raise Exception(f"Analysis job failed: {data.get('error')}")
                
        if i % 10 == 0:
            print(f"  ...still waiting (progress: {r.json().get('progress', 0)}%)")
            
    raise TimeoutError("Analysis did not complete in 60s")

if __name__ == "__main__":
    try:
        test_health()
        test_upload_and_analyze()
    except Exception as e:
        print(f"❌ Smoke test FAILED: {e}")
        exit(1)
