from __future__ import annotations

import os
from types import SimpleNamespace

from dotenv import load_dotenv

load_dotenv()


def _list_from_env(name: str) -> list:
    val = os.getenv(name, "")
    return [p.strip() for p in val.split(",") if p.strip()]


# Build DATABASE_URL from MYSQL_* variables if not explicitly set
_database_url = os.getenv("DATABASE_URL")
if not _database_url:
    mysql_host = os.getenv("MYSQL_HOST", "127.0.0.1")
    mysql_port = os.getenv("MYSQL_PORT", "3306")
    mysql_user = os.getenv("MYSQL_USER", "root")
    mysql_password = os.getenv("MYSQL_PASSWORD", "")
    mysql_db = os.getenv("MYSQL_DATABASE", "cd_ai_db")
    _database_url = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}?charset=utf8mb4"


settings = SimpleNamespace(
    PROJECT_NAME=os.getenv("PROJECT_NAME", "CD AI Backend"),
    VERSION=os.getenv("VERSION", "0.1.0"),
    DESCRIPTION=os.getenv("DESCRIPTION", "CD AI Backend API"),
    CORS_ORIGINS=_list_from_env("CORS_ORIGINS") or ["*"],
    HOST=os.getenv("HOST", "0.0.0.0"),
    PORT=int(os.getenv("PORT", "8000")),
    DEBUG=os.getenv("DEBUG", "false").lower() in ("1", "true", "yes"),
    # Enable automatic reload when running `python main.py` (or uvicorn programmatically)
    RELOAD=os.getenv("RELOAD", "false").lower() in ("1", "true", "yes"),
    DATABASE_URL=_database_url,
    ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")),
    SECRET_KEY=os.getenv("SECRET_KEY", "change-me"),
    ALGORITHM=os.getenv("ALGORITHM", "HS256"),
)
