# app/routers/auth.py
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, schemas
from app.deps import get_db, get_current_user
from app.core.security import hash_password, verify_password, create_access_token
from app.rate_limit import limiter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=schemas.UserOut, status_code=201)
@limiter.limit("10/minute")  # rate-limited => must include `request: Request`
def signup(
    request: Request,  # REQUIRED by SlowAPI
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    """Create a new user. Expects schemas.UserCreate(email, password[, role])."""
    existing = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = models.User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
    )
    # optional role support
    role_in: Optional[str] = getattr(user_in, "role", None)
    if role_in and hasattr(models.User, "role"):
        setattr(user, "role", role_in)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=schemas.Token)
@limiter.limit("5/minute")  # rate-limited => must include `request: Request`
def login(
    request: Request,  # REQUIRED by SlowAPI
    form_data: OAuth2PasswordRequestForm = Depends(),  # username = email
    db: Session = Depends(get_db),
):
    """Issue a JWT (Bearer). Send x-www-form-urlencoded: username=<email>&password=<pwd>."""
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    role = getattr(user, "role", "user")
    token = create_access_token(subject=user.email, extra={"role": role})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserOut)
def read_me(current_user: models.User = Depends(get_current_user)):
    """Return current user profile (requires Authorization: Bearer <token>)."""
    return current_user
