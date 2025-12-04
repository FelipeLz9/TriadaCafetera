from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Triada Cafetera API"
    DATABASE_URL: str = "sqlite+aiosqlite:///./triada_cafetera.db"
    SECRET_KEY: str = "clave_secreta_para_pruebas_cambiar_en_produccion"
    ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

settings = Settings()