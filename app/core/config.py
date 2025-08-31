from pydantic_settings import BaseSettings
from pydantic import AnyUrl
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "QuickQuickNotes API"
    debug: bool = False
    secret_key: str = "CHANGE_ME"
    access_token_exp_minutes: int = 60 * 24
    algorithm: str = "HS256"
    database_url: Optional[str] = None
    cors_origins: str = "*"  # comma-separated

    class Config:
        env_file = ".env"

settings = Settings()
