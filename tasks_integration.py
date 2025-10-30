import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# El único cambio de configuración: el permiso que pedimos ahora es para Tasks.
SCOPES = ["https://www.googleapis.com/auth/tasks"]

def get_tasks_service():
    """Autentica y crea un objeto de servicio para interactuar con la API de Tasks."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Aquí le decimos que construya el servicio de "tasks" en lugar de "keep"
        service = build("tasks", "v1", credentials=creds)
        return service
    except HttpError as err:
        print(err)
        return None

def create_shopping_list_task(shopping_list: dict):
    """Crea una nueva lista de tareas en Google Tasks con los ingredientes."""
    service = get_tasks_service()
    if not service:
        return {"error": "No se pudo conectar con el servicio de Tasks."}

    try:
        # 1. Crear una nueva lista de tareas para nuestra compra
        tasklist_body = {
            "title": "🛒 Lista de Compras - DietFlow"
        }
        tasklist = service.tasklists().insert(body=tasklist_body).execute()
        tasklist_id = tasklist.get("id")

        # 2. Añadir cada ingrediente como una tarea en esa nueva lista
        for nombre, data in shopping_list.items():
            task_body = {
                "title": f"{nombre} ({data['cantidad']} {data['unidad']})"
            }
            service.tasks().insert(tasklist=tasklist_id, body=task_body).execute()

        return {"success": True, "tasklist_id": tasklist_id}
    except HttpError as err:
        print(err)
        return {"success": False, "error": str(err)}

if __name__ == "__main__":
    print("Intentando autenticar con Google Tasks para generar 'token.json'...")
    service = get_tasks_service()
    if service:
        print("\n¡Autenticación exitosa! 'token.json' ha sido creado.")
    else:
        print("\nFalló la autenticación.")