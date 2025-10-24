from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.deps import get_db, get_token_payload
from app import models

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/stats")
def admin_stats(payload = Depends(get_token_payload), db: Session = Depends(get_db)):
    if payload.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    users = db.query(models.User).count()
    notes = db.query(models.Note).count()
    return {"users": users, "notes": notes}
