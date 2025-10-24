from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.deps import get_db, get_current_user
from app import models, schemas
from app.main import limiter  # 👈 Added limiter import

router = APIRouter(prefix="/api/notes", tags=["notes"])

def _get_or_create_tags(db: Session, tag_names: Optional[List[str]]) -> List[models.Tag]:
    if not tag_names:
        return []
    tags = []
    for name in set([n.strip().lower() for n in tag_names if n.strip()]):
        tag = db.query(models.Tag).filter(models.Tag.name == name).first()
        if not tag:
            tag = models.Tag(name=name)
            db.add(tag)
            db.flush()
        tags.append(tag)
    return tags

@router.post("/", response_model=schemas.NoteOut, status_code=201)
@limiter.limit("20/minute")  # 👈 Added rate limit here
def create_note(
    note_in: schemas.NoteCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    note = models.Note(
        title=note_in.title,
        content=note_in.content,
        owner_id=user.id
    )
    note.tags = _get_or_create_tags(db, note_in.tags)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

@router.get("/", response_model=List[schemas.NoteOut])
def list_notes(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
    q: Optional[str] = Query(None, description="Search in title/content"),
    tag: Optional[str] = Query(None, description="Filter by single tag"),
    archived: Optional[bool] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    stmt = select(models.Note).where(models.Note.owner_id == user.id)
    if archived is not None:
        stmt = stmt.where(models.Note.is_archived == archived)
    if q:
        like = f"%{q.lower()}%"
        stmt = stmt.where(
            (models.Note.title.ilike(like)) | (models.Note.content.ilike(like))
        )
    if tag:
        stmt = stmt.join(models.Note.tags).where(models.Tag.name == tag.lower())
    stmt = stmt.order_by(models.Note.updated_at.desc()).limit(limit).offset(offset)
    notes = db.execute(stmt).scalars().all()
    return notes

@router.get("/{note_id}", response_model=schemas.NoteOut)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    note = (
        db.query(models.Note)
        .filter(models.Note.id == note_id, models.Note.owner_id == user.id)
        .first()
    )
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=schemas.NoteOut)
def update_note(
    note_id: int,
    note_in: schemas.NoteUpdate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    note = (
        db.query(models.Note)
        .filter(models.Note.id == note_id, models.Note.owner_id == user.id)
        .first()
    )
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note_in.title is not None:
        note.title = note_in.title
    if note_in.content is not None:
        note.content = note_in.content
    if note_in.is_archived is not None:
        note.is_archived = note_in.is_archived
    if note_in.tags is not None:
        note.tags = _get_or_create_tags(db, note_in.tags)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

@router.delete("/{note_id}", status_code=204)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    note = (
        db.query(models.Note)
        .filter(models.Note.id == note_id, models.Note.owner_id == user.id)
        .first()
    )
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return None
