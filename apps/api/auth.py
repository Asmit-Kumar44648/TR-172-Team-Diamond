import os
import hashlib
from datetime import datetime, timezone
from typing import Optional, Dict, Any

from fastapi import Depends, HTTPException, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader

bearer_scheme = HTTPBearer(auto_error=False)
api_key_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)

DEMO_MODE = os.environ.get("DEMO_MODE", "true").lower() == "true"

# Supabase client — optional, only used in production
supabase = None
try:
    from supabase import create_client
    SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
    SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")
    if SUPABASE_URL and SUPABASE_SERVICE_KEY:
        supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        print("[Auth] Supabase client connected.")
    else:
        print("[Auth] Supabase credentials missing — running in offline mode.")
except Exception as e:
    print(f"[Auth] Supabase init failed: {e}")

JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", "demo-secret")

# Demo org context used when DEMO_MODE=true and no auth headers are provided
DEMO_ORG = {
    "org_id": "demo-org-001",
    "user_id": "demo-user-001",
    "plan": "pro",
    "daily_quota": 500,
    "auth_method": "demo",
}


def get_current_org(
    bearer: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    api_key_header: str = Security(api_key_scheme),
) -> Dict[str, Any]:
    """
    Dual-mode auth: Supabase JWT or API Key.
    Falls back to DEMO_ORG when DEMO_MODE=true and no credentials provided.
    """
    # ── DEMO fallback ──────────────────────────────────────────────────────────
    if DEMO_MODE and not bearer and not api_key_header:
        return DEMO_ORG

    # ── Bearer JWT ─────────────────────────────────────────────────────────────
    if bearer:
        if supabase is None and DEMO_MODE:
            return DEMO_ORG  # offline demo — just allow
        try:
            from jose import jwt, JWTError
            claims = jwt.decode(
                bearer.credentials, JWT_SECRET,
                algorithms=["HS256"],
                options={"verify_aud": False},
            )
            user_id = claims.get("sub")
            org_id = claims.get("org_id") or claims.get("app_metadata", {}).get("org_id")

            if supabase and org_id:
                resp = supabase.table("organizations").select("plan, daily_quota").eq("id", org_id).single().execute()
                plan = resp.data["plan"] if resp.data else "free"
                daily_quota = resp.data["daily_quota"] if resp.data else 5
            else:
                plan, daily_quota = "pro", 500

            return {"org_id": org_id or "unknown", "user_id": user_id,
                    "plan": plan, "daily_quota": daily_quota, "auth_method": "jwt"}
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid or expired JWT.")

    # ── API Key ────────────────────────────────────────────────────────────────
    if api_key_header:
        if not api_key_header.startswith("grsp_live_"):
            raise HTTPException(status_code=401, detail="Invalid API Key format.")
        if supabase is None:
            if DEMO_MODE:
                return DEMO_ORG
            raise HTTPException(status_code=500, detail="Database not configured.")

        key_hash = hashlib.sha256(api_key_header.encode()).hexdigest()
        resp = supabase.table("api_keys").select(
            "id, org_id, organizations(plan, daily_quota)"
        ).eq("key_hash", key_hash).is_("revoked_at", "null").single().execute()

        if not resp.data:
            raise HTTPException(status_code=401, detail="Invalid or revoked API Key.")

        key_id = resp.data["id"]
        supabase.table("api_keys").update(
            {"last_used_at": datetime.now(timezone.utc).isoformat()}
        ).eq("id", key_id).execute()

        return {
            "org_id": resp.data["org_id"],
            "api_key_id": key_id,
            "plan": resp.data["organizations"]["plan"],
            "daily_quota": resp.data["organizations"]["daily_quota"],
            "auth_method": "api_key",
        }

    raise HTTPException(status_code=401, detail="Missing authentication.")
