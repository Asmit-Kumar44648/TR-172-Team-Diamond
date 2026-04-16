from fastapi import FastAPI
from apps.api.main import app

for route in app.routes:
    if hasattr(route, 'methods'):
        print(f"[{','.join(route.methods)}] {route.path}")
