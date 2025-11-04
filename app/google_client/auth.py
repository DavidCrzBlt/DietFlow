import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from typing import Optional
from config import CREDENTIALS_FILE, TOKEN_FILE


SCOPES = ["https://www.googleapis.com/auth/tasks"]

def get_google_credentials() -> Optional[Credentials]:
    """
    Maneja el flujo de autenticación de Google y devuelve las credenciales.
    NO construye el servicio, solo maneja las credenciales.
    """
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refrescando token: {e}. Se pedirá uno nuevo.")
                creds = None # Fuerza a pedir uno nuevo
        
        if not creds: # Si falló el refresh o no existía
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Guarda el token (nuevo o refrescado)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return creds