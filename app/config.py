from pydantic_settings import BaseSettings, SettingsConfigDict
from zoneinfo import ZoneInfo
from pydantic import computed_field

class Settings(BaseSettings):
    """
    Define y carga todas las variables de entorno de la aplicación.
    """
    # Le decimos a Pydantic que lea nuestro archivo .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str
    
    TIMEZONE: str = "America/Mexico_City"

    @computed_field
    @property
    def TZ(self) -> ZoneInfo:
        return ZoneInfo(self.TIMEZONE)

settings = Settings()