from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.requests import Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from secure import SecureHeaders

from app.core.config import settings
from app.db import Base, engine
from app.routers.notes import router as notes_router
from app.routers.auth import router as auth_router
from app.routers import admin


# ---- Initialize FastAPI ----
app = FastAPI(
    title=settings.app_name,
    version="2.0.0",
    contact={"name": "QuickNotes API", "url": "https://example.com"},
    description="A polished, secure, and test-covered QuickNotes API built with FastAPI.",
)


# ---- Security Headers ----
secure_headers = SecureHeaders()

@app.middleware("http")
async def set_security_headers(request, call_next):
    resp = await call_next(request)
    secure_headers.starlette(
        resp,
        referrer="no-referrer",
        server="",
        content_security_policy="default-src 'none'; frame-ancestors 'none';"
    )
    return resp


# ---- Body Size Limit ----
class BodySizeLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_bytes=1_000_000):
        super().__init__(app)
        self.max_bytes = max_bytes

    async def dispatch(self, request, call_next):
        body = await request.body()
        if len(body) > self.max_bytes:
            return JSONResponse({"detail": "Payload too large"}, status_code=413)
        request._body = body
        return await call_next(request)

app.add_middleware(BodySizeLimitMiddleware, max_bytes=1_000_000)


# ---- Rate Limiting ----
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

def rl_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse({"detail": "Too many requests"}, status_code=429)

app.add_exception_handler(RateLimitExceeded, rl_handler)


# ---- HTTPS Redirect (enable only in production) ----
# app.add_middleware(HTTPSRedirectMiddleware)


# ---- CORS ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---- Routers ----
app.include_router(admin.router)
app.include_router(auth_router)
app.include_router(notes_router)


# ---- Startup ----
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


# ---- Health Check ----
@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
