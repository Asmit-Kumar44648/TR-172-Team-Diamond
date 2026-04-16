import secrets
import hashlib
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from apps.api.auth import get_current_org, supabase

router = APIRouter(prefix="/v1/auth/api-keys", tags=["api_keys"])

class CreateKeyRequest(BaseModel):
    name: str
    
    model_config = {"extra": "forbid"}

class APIKeyResponse(BaseModel):
    id: str
    name: str
    prefix: str
    created_at: str
    last_used_at: Optional[str]
    revoked_at: Optional[str]
    # The actual key is only returned ONCE during creation
    key: Optional[str] = None


@router.post("", response_model=APIKeyResponse)
async def create_api_key(request: CreateKeyRequest, current_org: dict = Depends(get_current_org)):
    # Standard security measure: only allow token generation via JWT auth, not via another API key
    if current_org.get("auth_method") == "api_key":
         raise HTTPException(status_code=403, detail="Cannot generate API keys using an API key. Please use dashboard.")
         
    org_id = current_org["org_id"]
    
    # Generate URL-safe 32 byte string
    raw_token = secrets.token_urlsafe(32)
    full_key = f"grsp_live_{raw_token}"
    
    key_prefix = full_key[:20]
    key_hash = hashlib.sha256(full_key.encode()).hexdigest()
    
    if supabase:
        record = {
            "org_id": org_id,
            "name": request.name,
            "key_hash": key_hash,
            "key_prefix": key_prefix
        }
        resp = supabase.table("api_keys").insert(record).execute()
        
        if not resp.data:
            raise HTTPException(status_code=500, detail="Failed to create API key")
            
        data = resp.data[0]
        
        return APIKeyResponse(
            id=data["id"],
            name=data["name"],
            prefix=data["key_prefix"],
            created_at=data["created_at"],
            key=full_key # Emitted ONCE
        )
    
    # Fallback if no DB
    return APIKeyResponse(
        id="dummy_id", name=request.name, prefix=key_prefix, created_at=datetime.now(timezone.utc).isoformat(), key=full_key
    )

@router.get("", response_model=List[APIKeyResponse])
async def list_api_keys(current_org: dict = Depends(get_current_org)):
    org_id = current_org["org_id"]
    if supabase:
        resp = supabase.table("api_keys").select("id, name, key_prefix, created_at, last_used_at, revoked_at").eq("org_id", org_id).execute()
        
        return [
            APIKeyResponse(
                id=r["id"],
                name=r["name"],
                prefix=r["key_prefix"],
                created_at=r["created_at"],
                last_used_at=r["last_used_at"],
                revoked_at=r["revoked_at"]
            )
            for r in resp.data
        ]
    return []

@router.delete("/{key_id}")
async def revoke_api_key(key_id: str, current_org: dict = Depends(get_current_org)):
    org_id = current_org["org_id"]
    if supabase:
        # Revoke instead of hard delete
        now_str = datetime.now(timezone.utc).isoformat()
        supabase.table("api_keys").update({"revoked_at": now_str}).eq("id", key_id).eq("org_id", org_id).execute()
        
    return {"revoked": True}
