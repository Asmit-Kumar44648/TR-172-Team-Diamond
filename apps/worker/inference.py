import modal

stub = modal.Stub("grasp-inference")

image = (
    modal.Image.from_registry("nvidia/cuda:12.1.0-devel-ubuntu22.04")
    .pip_install([
        "torch==2.2.0", "torchvision", "open3d==0.18.0",
        "numpy", "scipy", "networkx", "ripser",
        "opencv-python-headless", "anthropic",
        "pybullet", "fastapi", "supabase"
    ])
    .run_commands([
        "git clone https://github.com/NVlabs/contact_graspnet /opt/contact_graspnet",
        "cd /opt/contact_graspnet && pip install -e ."
    ])
)

@stub.cls(
    gpu=modal.gpu.A10G(),
    image=image,
    timeout=120,
    container_idle_timeout=300,
    volumes={"/models": modal.Volume.from_name("grasp-models")},
    secrets=[modal.Secret.from_name("grasp-secrets")]
)
class GraspInference:
    def __enter__(self):
        # Cold start — load models once
        import torch
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # SAM2 + Contact-GraspNet loaded here
        # (mock implementations for now — real weights at /models/)
        print(f"GRASP inference worker ready on {self.device}")
    
    @modal.method()
    def run(self, job_payload: dict) -> dict:
        from packages.pipeline.pipeline import run_full_pipeline
        return run_full_pipeline(job_payload, self.device)
