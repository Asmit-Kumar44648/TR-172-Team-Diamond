import sys
import os

# Ensure monorepo packages are accessible directly when testing locally
_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
if _root not in sys.path:
    sys.path.insert(0, _root)

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from apps.api.middleware.monitoring import MonitoringMiddleware
from apps.api.routers import scenes, analysis, export, keys, webhooks

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("GRASP API starting up...")
    yield
    print("GRASP API shutting down...")

app = FastAPI(
    title="GRASP API",
    version="1.0.0",
    description="Grasp Reliability & Safety Platform — API Backend",
    lifespan=lifespan
)

# 1. Monitoring & Timing Middleware
app.add_middleware(MonitoringMiddleware)

# 2. CORS — allow all in dev/demo mode so the local demo.html can call the API
DEMO_MODE = os.environ.get("DEMO_MODE", "true").lower() == "true"
# Support dynamic Vercel URLs and local dev
ALLOWED_ORIGINS = ["*"] if DEMO_MODE else [
    o for o in os.environ.get("ALLOWED_ORIGINS", "").split(",") if o
] + [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://*.vercel.app"  # Regex or exact match? (FastAPI CORSMiddleware doesn't do wildcards in the list, but we can do allow_origin_regex)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if "*" not in ALLOWED_ORIGINS else ["*"],
    allow_origin_regex=os.environ.get("ALLOWED_ORIGIN_REGEX", "https://.*\.vercel\.app"),
    allow_credentials=not ("*" in ALLOWED_ORIGINS),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(scenes.router)
app.include_router(analysis.router)
app.include_router(export.router)
app.include_router(keys.router)
app.include_router(webhooks.router)

@app.get("/health")
async def health_check():
    from apps.api.auth import supabase
    from apps.api.rate_limit import redis
    return {
        "status": "ok",
        "version": "1.0.0",
        "demo_mode": DEMO_MODE,
        "supabase_connected": supabase is not None,
        "redis_connected": redis is not None,
    }
