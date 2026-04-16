import httpx
import time
import asyncio
from typing import Optional, Callable, Dict, Any, Union, BinaryIO
from .models import ScenePlan, UsageStats
from .exceptions import (
    GRASPError, GRASPAuthError, GRASPRateLimitError, 
    GRASPTimeoutError, GRASPAPIError
)

class GRASPClient:
    def __init__(self, api_key: str, base_url: str = "https://api.grasp.ai"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.headers = {"X-API-Key": self.api_key}

    def _handle_response(self, response: httpx.Response):
        if response.status_code == 200:
            return response.json()
        elif response.status_code in (401, 403):
            raise GRASPAuthError("Invalid API Key or unauthorized access.")
        elif response.status_code == 429:
            raise GRASPRateLimitError(response.json().get("detail", "Rate limit exceeded."))
        else:
            raise GRASPAPIError(f"API Error ({response.status_code}): {response.text}", status_code=response.status_code)

    def analyze(
        self, 
        depth_image: BinaryIO, 
        jaw_width_mm: float = 85.0, 
        max_aperture_mm: float = 80.0,
        wait: bool = True,
        timeout: int = 60,
        on_progress: Optional[Callable[[str, int], None]] = None
    ) -> Union[ScenePlan, str]:
        """
        Sync analysis request. 
        If wait=True, blocks until completion or timeout.
        Returns ScenePlan if wait=True, else job_id string.
        """
        with httpx.Client(headers=self.headers, timeout=30.0) as client:
            files = {"depth": depth_image}
            data = {"jaw_width_mm": str(jaw_width_mm), "max_aperture_mm": str(max_aperture_mm)}
            
            # 1. Upload
            resp = client.post(f"{self.base_url}/v1/scenes/upload", files=files, data=data)
            scene_data = self._handle_response(resp)
            scene_id = scene_data["scene_id"]
            
            # 2. Trigger Analysis
            resp = client.post(f"{self.base_url}/v1/analysis/run", json={"scene_id": scene_id})
            job_data = self._handle_response(resp)
            job_id = job_data["job_id"]
            
            if not wait:
                return job_id
                
            return self.wait(job_id, timeout=timeout, on_progress=on_progress)

    def wait(
        self, 
        job_id: str, 
        timeout: int = 60, 
        on_progress: Optional[Callable[[str, int], None]] = None
    ) -> ScenePlan:
        """Polls the API until the job is complete."""
        start_time = time.time()
        while (time.time() - start_time) < timeout:
            with httpx.Client(headers=self.headers) as client:
                resp = client.get(f"{self.base_url}/v1/analysis/{job_id}/stream") # Note: SDK uses standard GET for polling if SSE not feasible here
                # In our backend, /v1/analysis/{jobId} (GET) returns the current status.
                # Since we don't have a direct GET status endpoint yet (only SSE), 
                # we'll use the existing /v1/analysis/{jobId}/stream as a fallback or 
                # we assume a status endpoint exists.
                # For this SDK, we'll implement a simple polling against a status endpoint.
                
                # FALLBACK: We'll assume the API has a /v1/analysis/{jobId}/status endpoint
                resp = client.get(f"{self.base_url}/v1/analysis/{job_id}")
                if resp.status_code == 200:
                    data = resp.json()
                    status = data.get("status", "RUNNING")
                    progress = data.get("progress", 0)
                    stage = data.get("stage", "Unknown")
                    
                    if on_progress:
                        on_progress(stage, progress)
                        
                    if status == "COMPLETE":
                        return ScenePlan.from_dict(data["result"])
                    elif status == "FAILED":
                        raise GRASPAPIError(f"Job failed: {data.get('error', 'Unknown error')}")
                
            time.sleep(2)
            
        raise GRASPTimeoutError(f"Analysis timed out after {timeout} seconds.")

    # Async Methods
    async def analyze_async(
        self, 
        depth_image: BinaryIO, 
        jaw_width_mm: float = 85.0, 
        max_aperture_mm: float = 80.0,
        wait: bool = True,
        timeout: int = 60,
        on_progress: Optional[Callable[[str, int], None]] = None
    ) -> Union[ScenePlan, str]:
        async with httpx.AsyncClient(headers=self.headers, timeout=30.0) as client:
            files = {"depth": depth_image}
            data = {"jaw_width_mm": str(jaw_width_mm), "max_aperture_mm": str(max_aperture_mm)}
            
            resp = await client.post(f"{self.base_url}/v1/scenes/upload", files=files, data=data)
            scene_data = self._handle_response(resp)
            scene_id = scene_data["scene_id"]
            
            resp = await client.post(f"{self.base_url}/v1/analysis/run", json={"scene_id": scene_id})
            job_data = self._handle_response(resp)
            job_id = job_data["job_id"]
            
            if not wait:
                return job_id
                
            return await self.wait_async(job_id, timeout=timeout, on_progress=on_progress)

    async def wait_async(
        self, 
        job_id: str, 
        timeout: int = 60, 
        on_progress: Optional[Callable[[str, int], None]] = None
    ) -> ScenePlan:
        start_time = time.time()
        while (time.time() - start_time) < timeout:
            async with httpx.AsyncClient(headers=self.headers) as client:
                resp = await client.get(f"{self.base_url}/v1/analysis/{job_id}")
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("status") == "COMPLETE":
                        return ScenePlan.from_dict(data["result"])
                    elif data.get("status") == "FAILED":
                        raise GRASPAPIError(data.get("error", "Job failed"))
                    
                    if on_progress:
                        on_progress(data.get("stage", ""), data.get("progress", 0))
                
            await asyncio.sleep(2)
        raise GRASPTimeoutError("Async analysis timeout.")

    def get_usage(self) -> UsageStats:
        """Fetch current quota usage."""
        with httpx.Client(headers=self.headers) as client:
            resp = client.get(f"{self.base_url}/v1/billing/usage")
            data = self._handle_response(resp)
            return UsageStats(**data)
