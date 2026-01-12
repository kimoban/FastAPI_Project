from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "FastAPI Project"
    environment: str = "development"
    database_url: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/fastapi_db",
        validation_alias="DATABASE_URL",
    )
    secret_key: str = Field(default="change_me", validation_alias="SECRET_KEY")
    algorithm: str = Field(default="HS256", validation_alias="ALGORITHM")
    access_token_expire_minutes: int = Field(default=60, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES")


@lru_cache
def get_settings() -> Settings:
    return Settings()
