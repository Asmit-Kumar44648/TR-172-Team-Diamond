import os
from pathlib import Path

# Fix 1: Create missing __init__.py files so package paths resolve without relative import crashes
for path in ['apps', 'apps/api', 'packages']:
    init_path = Path(path) / '__init__.py'
    init_path.parent.mkdir(parents=True, exist_ok=True)
    if not init_path.exists():
        init_path.touch()

# Fix 2: Convert relative imports to absolute monorepo imports in all Routers and Main
def apply_fix(file_path, replaces):
    path = Path(file_path)
    if path.exists():
        content = path.read_text()
        original = content
        for old, new in replaces:
            content = content.replace(old, new)
        if content != original:
            path.write_text(content)
            print(f"Fixed {file_path}")

routers = ['scenes.py', 'analysis.py', 'export.py', 'keys.py', 'billing.py', 'webhooks.py']
for router in routers:
    apply_fix(f"apps/api/routers/{router}", [
        ("from ..auth", "from apps.api.auth"),
        ("from ..rate_limit", "from apps.api.rate_limit"),
        ("from schema.models", "from packages.schema.models") # In export.py
    ])

apply_fix("apps/api/main.py", [
    ("from routers import", "from apps.api.routers import")
])

apply_fix("apps/api/tests/test_api.py", [
    ("from ..main", "from apps.api.main"),
    ("from ..auth", "from apps.api.auth")
])

apply_fix("packages/pipeline/pipeline.py", [
    ("from schema.models", "from packages.schema.models"),
    # Fix 3: Numpy Float64 Serialization Crash on Grasp Position
    ('"position": {"x": g["pose"][0,3], "y": g["pose"][1,3], "z": g["pose"][2,3]},', '"position": {"x": float(g["pose"][0,3]), "y": float(g["pose"][1,3]), "z": float(g["pose"][2,3])},')
])

apply_fix("apps/worker/tests/test_pipeline.py", [
    ("from schema.models", "from packages.schema.models")
])

