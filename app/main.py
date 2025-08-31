from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db import Base, engine
from app.routers.notes import router as notes_router
from app.routers.auth import router as auth_router

app = FastAPI(
    title=settings.app_name,
    version="2.0.0",
    contact={"name": "QuickNotes API", "url": "https://example.com"},
    description="A polished, secure, and test-covered QuickNotes API built with FastAPI.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}

app.include_router(auth_router)
app.include_router(notes_router)
