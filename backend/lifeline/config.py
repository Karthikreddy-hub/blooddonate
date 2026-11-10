import os
from sqlalchemy import URL


class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "local-development-only-change-me")
    SQLALCHEMY_DATABASE_URI = URL.create(
        drivername="postgresql+psycopg",
        username=os.getenv("POSTGRES_USER", "lifeline"),
        password=os.getenv("POSTGRES_PASSWORD", "lifeline"),
        host=os.getenv("DATABASE_HOST", "localhost"),
        port=int(os.getenv("DATABASE_PORT", "5432")),
        database=os.getenv("POSTGRES_DB", "lifeline"),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True, "pool_recycle": 300}
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024
    WTF_CSRF_TIME_LIMIT = 3600
