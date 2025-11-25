from pydantic_settings import BaseSettings, SettingsConfigDict
from zoneinfo import ZoneInfo
from pydantic import computed_field
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

SECRETS_DIR = BASE_DIR / "secrets"
CREDENTIALS_FILE = SECRETS_DIR / "credentials.json"
TOKEN_FILE = SECRETS_DIR / "token.json"

# --- Google Configuration ---
GOOGLE_SCOPES = ["https://www.googleapis.com/auth/tasks"]

class Settings(BaseSettings):
    """
    Define y carga todas las variables de entorno de la aplicación.
    """
    # Le decimos a Pydantic que lea nuestro archivo .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    
    TIMEZONE: str = "America/Mexico_City"

    @computed_field
    @property
    def TZ(self) -> ZoneInfo:
        return ZoneInfo(self.TIMEZONE)

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()