"""Load local settings without mutating or printing credentials."""
import os
from dataclasses import dataclass, field
from pathlib import Path
from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    database_url: str = "sqlite:///./editorial.db"
    gemini_api_key: str = field(default="", repr=False)
    gemini_model: str = "gemini-3.8-flash"
    ai_timeout_seconds: int = 60
    ai_max_input_chars: int = 80000
    ai_max_output_tokens: int = 8192
    ai_daily_request_limit: int = 20
    workspace_password: str = field(default="", repr=False)
    session_secret: str = field(default="", repr=False)
    cors_origins: tuple = ("http://localhost:5173", "http://127.0.0.1:5173")
    cloud: bool = False


def get_settings():
    values = {}
    for candidate in (ROOT / "backend/.env", ROOT / ".env", ROOT / ".env.local"):
        if candidate.is_file():
            values.update({key: value for key, value in dotenv_values(candidate).items() if value is not None})
    values.update(os.environ)
    def positive(key, default, upper):
        try:
            value = int(values.get(key, default))
        except (TypeError, ValueError):
            raise ValueError(f"{key} must be a positive integer.") from None
        if not 1 <= value <= upper:
            raise ValueError(f"{key} must be between 1 and {upper}.")
        return value
    url = values.get("DATABASE_URL") or values.get("POSTGRES_URL") or "sqlite:///./editorial.db"
    if url.startswith(("postgres://", "postgresql://")):
        url = "postgresql+psycopg://" + url.split("://", 1)[1]
    return Settings(database_url=url, gemini_api_key=values.get("GEMINI_API_KEY", "").strip(),
                    gemini_model=values.get("GEMINI_MODEL") or "gemini-3.8-flash",
                    ai_timeout_seconds=positive("AI_TIMEOUT_SECONDS", 60, 120),
                    ai_max_input_chars=positive("AI_MAX_INPUT_CHARS", 80000, 200000),
                    ai_max_output_tokens=positive("AI_MAX_OUTPUT_TOKENS", 8192, 16000),
                    ai_daily_request_limit=positive("AI_DAILY_REQUEST_LIMIT", 20, 200),
                    workspace_password=values.get("WORKSPACE_PASSWORD", ""),
                    session_secret=values.get("SESSION_SECRET", ""),
                    cors_origins=tuple(origin.strip() for origin in values.get("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",") if origin.strip()),
                    cloud=values.get("VERCEL") == "1")
