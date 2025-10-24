from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.requests import Request
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.db import Base, engine
from app.rate_limit import limiter
from app.routers import admin
from app.routers.auth import router as auth_router
from app.routers.notes import router as notes_router

app = FastAPI(
    title=getattr(settings, "app_name", "QuickNotes API"),
    version="2.0.0",
    contact={"name": "QuickNotes API", "url": "https://example.com"},
    description="A polished, secure, and test-covered QuickNotes API built with FastAPI.",
)

# ---- Body size limit ----
class BodySizeLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_bytes: int = 1_000_000):
        super().__init__(app)
        self.max_bytes = max_bytes
    async def dispatch(self, request, call_next):
        body = await request.body()
        if len(body) > self.max_bytes:
            return JSONResponse({"detail": "Payload too large"}, status_code=413)
        request._body = body
        return await call_next(request)
app.add_middleware(BodySizeLimitMiddleware, max_bytes=1_000_000)

# ---- Rate limiting ----
def rl_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse({"detail": "Too many requests"}, status_code=429)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rl_handler)

# ---- Security headers (manual) ----
@app.middleware("http")
async def set_security_headers(request, call_next):
    resp = await call_next(request)
    h = resp.headers
    h["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
    h["X-Frame-Options"] = "DENY"
    h["X-Content-Type-Options"] = "nosniff"
    h["Referrer-Policy"] = "no-referrer"
    h["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none';"
    return resp

# ---- CORS ----
try:
    cors_origins = [o.strip() for o in getattr(settings, "cors_origins", "*").split(",") if o.strip()]
except Exception:
    cors_origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
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

# ---- Health ----
@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
