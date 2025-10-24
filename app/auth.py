from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.deps import get_db
from app import models, schemas
from app.auth import hash_password, verify_password, create_access_token
from app.main import limiter
from app.audit import audit

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=schemas.UserOut, status_code=201)
def signup(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    if db.query(models.User).filter(models.User.email == user_in.email).first():
        audit("signup_failed", email=user_in.email, reason="Email already registered")
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    user = models.User(email=user_in.email, hashed_password=hash_password(user_in.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    audit("signup_success", email=user.email)
    return user


@router.post("/login", response_model=schemas.Token)
@limiter.limit("5/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        audit("login_failed", email=form_data.username, ip=request.client.host)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    token = create_access_token(subject=user.email)
    audit("login_success", email=user.email, ip=request.client.host)
    return {"access_token": token, "token_type": "bearer"}
