from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

# Map to your config names
SECRET_KEY = getattr(settings, "secret_key", getattr(settings, "SECRET_KEY", "dev-secret"))
ALGORITHM = getattr(settings, "algorithm", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = getattr(settings, "access_token_exp_minutes", 60)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(subject: str, extra: Optional[Dict[str, Any]] = None,
                        expires_minutes: Optional[int] = None) -> str:
    to_encode: Dict[str, Any] = {"sub": str(subject)}
    if extra:
        to_encode.update(extra)
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes or ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
