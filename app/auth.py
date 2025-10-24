# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, schemas
from app.deps import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.rate_limit import limiter

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=schemas.UserOut, status_code=201)
def signup(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # email uniqueness
    if db.query(models.User).filter(models.User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = models.User(email=user_in.email, hashed_password=hash_password(user_in.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=schemas.Token)
@limiter.limit("5/minute")
def login(
    request: Request,  # <-- REQUIRED for SlowAPI
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    # Put role claim in the token if your model has it; else default to "user"
    role = getattr(user, "role", "user")
    token = create_access_token(subject=user.email, extra={"role": role})
    return {"access_token": token, "token_type": "bearer"}
