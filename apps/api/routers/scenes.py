from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from typing import Optional
import uuid
import os

from apps.api.auth import get_current_org, supabase
from apps.api.rate_limit import get_plan_limits

router = APIRouter(prefix="/v1/scenes", tags=["scenes"])

NUMPY_MAGIC_BYTES = b"\x93NUMPY"
PNG_MAGIC_BYTES    = b"\x89PNG\r\n\x1a\n"
DEMO_MODE = os.environ.get("DEMO_MODE", "true").lower() == "true"


@router.post("/upload")
async def upload_scene(
    depth: UploadFile = File(...),
    rgb: Optional[UploadFile] = File(None),
    jaw_width_mm: float = Form(85.0),
    max_aperture_mm: float = Form(80.0),
    current_org: dict = Depends(get_current_org),
):
    plan   = current_org["plan"]
    org_id = current_org["org_id"]
    user_id = current_org.get("user_id")

    # File-size validation
    _, max_upload_size_mb = get_plan_limits(plan)
    max_upload_size_bytes = max_upload_size_mb * 1024 * 1024

    # Magic-byte validation
    header = await depth.read(8)
    await depth.seek(0)
    if not (header[:6] == NUMPY_MAGIC_BYTES or header[:8] == PNG_MAGIC_BYTES):
        raise HTTPException(
            status_code=400,
            detail="Invalid depth file. Must be a NumPy (.npy/.npz) or PNG file.",
        )

    # Get file size without consuming the stream
    depth.file.seek(0, 2)
    depth_size = depth.file.tell()
    depth.file.seek(0)
    if depth_size > max_upload_size_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Plan '{plan}' allows max {max_upload_size_mb} MB.",
        )

    # Clamp gripper params
    jaw_width_mm    = max(10.0, min(300.0, jaw_width_mm))
    max_aperture_mm = max(10.0, min(300.0, max_aperture_mm))

    scene_id = str(uuid.uuid4())
    depth_ext = (depth.filename or "depth.npz").rsplit(".", 1)[-1]
    depth_path = f"{org_id}/{scene_id}/depth.{depth_ext}"
    rgb_path = None

    if supabase and not DEMO_MODE:
        depth.file.seek(0)
        supabase.storage.from_("scenes").upload(depth_path, depth.file.read())

        if rgb:
            rgb_ext = (rgb.filename or "rgb.png").rsplit(".", 1)[-1]
            rgb_path = f"{org_id}/{scene_id}/rgb.{rgb_ext}"
            supabase.storage.from_("scenes").upload(rgb_path, await rgb.read())

        if not user_id:
            ur = supabase.table("users").select("id").eq("org_id", org_id).limit(1).execute()
            user_id = ur.data[0]["id"] if ur.data else None

        if user_id:
            supabase.table("scenes").insert({
                "id": scene_id,
                "org_id": org_id,
                "uploaded_by": user_id,
                "name": depth.filename,
                "status": "uploaded",
                "depth_storage_path": depth_path,
                "rgb_storage_path": rgb_path,
                "jaw_width_mm": jaw_width_mm,
                "max_aperture_mm": max_aperture_mm,
            }).execute()

    return {
        "scene_id": scene_id,
        "status": "uploaded",
        "name": depth.filename,
        "jaw_width_mm": jaw_width_mm,
        "max_aperture_mm": max_aperture_mm,
        "demo_mode": DEMO_MODE,
    }
