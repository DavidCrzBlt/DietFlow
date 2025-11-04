from google_client.auth import get_google_credentials
from google_client.client import GoogleTasksClient
from repositories.config_repo import ConfigRepository
from database import get_db
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session



def get_google_client() -> GoogleTasksClient:
    creds = get_google_credentials()
    if not creds:
        raise HTTPException(status_code=503, detail="No se pudo autenticar con Google")
    return GoogleTasksClient(creds)

def get_config_repo(db: Session = Depends(get_db)) -> ConfigRepository:
    return ConfigRepository(db)