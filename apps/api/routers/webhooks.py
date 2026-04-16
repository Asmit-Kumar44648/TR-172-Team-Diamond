import secrets
import hashlib
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from pydantic import HttpUrl

from apps.api.auth import get_current_org, supabase

router = APIRouter(prefix="/v1/webhooks", tags=["webhooks"])

class CreateWebhookRequest(BaseModel):
    url: HttpUrl
    events: List[str] = ["job.completed", "job.failed"]
    
    model_config = {"extra": "forbid"}

class WebhookResponse(BaseModel):
    id: str
    url: str
    events: List[str]
    enabled: bool
    secret: Optional[str] = None # Only populated on creation

@router.post("", response_model=WebhookResponse)
async def create_webhook(request: CreateWebhookRequest, current_org: dict = Depends(get_current_org)):
    org_id = current_org["org_id"]
    
    # Generate webhook secret
    raw_secret = f"whsec_{secrets.token_urlsafe(24)}"
    secret_hash = hashlib.sha256(raw_secret.encode()).hexdigest()
    
    if supabase:
        record = {
            "org_id": org_id,
            "url": str(request.url),
            "secret_hash": secret_hash,
            "events": request.events,
            "enabled": True
        }
        
        resp = supabase.table("webhooks").insert(record).execute()
        if not resp.data:
             raise HTTPException(status_code=500, detail="Failed to create webhook")
             
        data = resp.data[0]
        
        return WebhookResponse(
             id=data["id"],
             url=data["url"],
             events=data["events"],
             enabled=data["enabled"],
             secret=raw_secret
        )
        
    return WebhookResponse(id="dummy", url=str(request.url), events=request.events, enabled=True, secret=raw_secret)

@router.get("", response_model=List[WebhookResponse])
async def list_webhooks(current_org: dict = Depends(get_current_org)):
    org_id = current_org["org_id"]
    if supabase:
        resp = supabase.table("webhooks").select("id, url, events, enabled").eq("org_id", org_id).execute()
        return [
             WebhookResponse(
                  id=r["id"],
                  url=r["url"],
                  events=r["events"],
                  enabled=r["enabled"]
             ) for r in resp.data
        ]
    return []

@router.delete("/{webhook_id}")
async def delete_webhook(webhook_id: str, current_org: dict = Depends(get_current_org)):
    org_id = current_org["org_id"]
    if supabase:
        supabase.table("webhooks").delete().eq("id", webhook_id).eq("org_id", org_id).execute()
    return {"deleted": True}
