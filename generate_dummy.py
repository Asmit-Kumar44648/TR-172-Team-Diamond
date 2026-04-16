import numpy as np
import os

if not os.path.exists('ml/demo_scenes'):
    os.makedirs('ml/demo_scenes')

def make_scene(name, is_cluttered=False):
    depth = np.random.uniform(0.3, 2.0, (480, 640)).astype(np.float32)
    rgb = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    intrinsics = {"fx": 525.0, "fy": 525.0, "cx": 319.5, "cy": 239.5}
    jaw_width_mm = 85.0
    max_aperture_mm = 80.0
    
    np.savez_compressed(
        f"ml/demo_scenes/{name}.npz",
        depth=depth,
        rgb=rgb,
        intrinsics=intrinsics,
        jaw_width_mm=jaw_width_mm,
        max_aperture_mm=max_aperture_mm
    )

make_scene("demo_easy")
make_scene("demo_medium")
make_scene("demo_cluttered", True)
print("Dummy data generated.")
