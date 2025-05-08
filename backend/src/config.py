import os

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "tutor.ua"
    BACKEND_CORS_ORIGINS: list[str] = os.environ.get(  # type: ignore
        "BACKEND_CORS_ORIGINS",
        [
            "http://localhost:8000",
            "https://localhost:8000",
            "http://localhost",
            "https://localhost",
            "http://0.0.0.0:8080",
            "http://localhost:3000",
        ],
    )
    SERVER_PORT: int = 8000
    SERVER_HOST: str = "0.0.0.0"

    DB_NAME: str = os.environ.get("DB_NAME", "postgres")
    DB_USER: str = os.environ.get("DB_USER", "postgres")
    DB_PASSWORD: str = os.environ.get("DB_PASSWORD", "postgres")
    DB_HOST: str = os.environ.get("DB_HOST", "database")
    DB_PORT: int = int(os.environ.get("DB_PORT", 5432))

    DATABASE_URL: str = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    ECHO_SQL: bool = True

    REDIS_URL: str = os.environ.get("REDIS_URL", "redis://:redispass@redis:6379/0")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", int(60 * 24))
    )  # 1 day
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(
        os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES", int(60 * 24 * 7))
    )  # 7 days
    ADMIN_TOKEN_EXPIRE_MINUTES: int = int(
        os.environ.get("ADMIN_TOKEN_EXPIRE_MINUTES", int(60 * 24 * 7))
    )  # 7 days
    ROTATE_REFRESH_TOKEN: bool = bool(os.environ.get("ROTATE_REFRESH_TOKEN", False))
    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str = os.environ.get(
        "JWT_SECRET_KEY", "develop"
    )  # should be kept secret

    class Config:
        case_sensitive = True
        env_file = ".env"

    @field_validator("BACKEND_CORS_ORIGINS")
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


settings = Settings()
