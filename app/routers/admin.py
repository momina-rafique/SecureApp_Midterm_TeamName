from fastapi import APIRouter, Depends
from app.authz import require_role

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/stats", dependencies=[Depends(require_role("admin"))])
async def stats():
    return {"ok": True}
