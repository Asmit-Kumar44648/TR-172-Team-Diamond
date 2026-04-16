# GRASP Python SDK

The official Python client for the [GRASP Platform](https://grasp.ai). Audit and validate robot grasps for reliability and safety before execution.

## Installation

```bash
pip install grasp-sdk
```

## Quick Start (Sync)

```python
from grasp import GRASPClient

client = GRASPClient(api_key="your_api_key_here")

# blocks until analysis is complete
with open("scene.npz", "rb") as f:
    result = client.analyze(f, jaw_width_mm=85.0)

print(f"Audit finished in {result.inference_time_seconds}s")
for grasp in result.top_10_grasps:
    status = "REJECTED" if grasp.rejected else "OK"
    print(f"Rank {grasp.rank} [{status}]: {grasp.audit.explanation}")
    
# Export for ROS MoveIt
result.to_ros_json("plan.json")
```

## Async Usage

```python
import asyncio
from grasp import GRASPClient

async def main():
    client = GRASPClient(api_key="your_api_key_here")
    
    with open("scene.npz", "rb") as f:
        # non-blocking trigger
        job_id = await client.analyze_async(f, wait=False)
        print(f"Job triggered: {job_id}")
        
        # wait with progress callback
        result = await client.wait_async(job_id, on_progress=lambda s, p: print(f"{s}: {p}%"))
        print(f"Safe Ratio: {result.collision_free_ratio}")

asyncio.run(main())
```

## Error Handling

```python
from grasp import GRASPClient, GRASPAuthError, GRASPRateLimitError

client = GRASPClient(api_key="invalid")
try:
    client.get_usage()
except GRASPAuthError:
    print("Check your API key.")
```

## License
MIT
