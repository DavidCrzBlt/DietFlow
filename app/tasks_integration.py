import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from sqlalchemy.orm import Session
from models import Configuracion 

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

# ... (el resto del archivo no cambia)

def update_or_create_shopping_list(db: Session, shopping_list: dict):
    """
    Busca la lista de compras de DietFlow, la limpia y la actualiza.
    Si no existe, la crea y guarda su ID.
    """
    service = get_tasks_service()
    if not service:
        return {"error": "No se pudo conectar con el servicio de Tasks."}

    config_entry = db.query(Configuracion).filter(Configuracion.clave == "tasklist_id").first()
    tasklist_id = config_entry.valor if config_entry else None

    try:
        if tasklist_id:
            print(f"Encontrado ID de lista: {tasklist_id}. Limpiando tareas existentes...")
            
            # ===== INICIO DEL CÓDIGO CORREGIDO =====
            page_token = None
            while True:
                tasks_result = service.tasks().list(
                    tasklist=tasklist_id, 
                    pageToken=page_token
                ).execute()
                
                tasks = tasks_result.get("items", [])
                for task in tasks:
                    service.tasks().delete(tasklist=tasklist_id, task=task.get("id")).execute()

                # Verificamos si hay más páginas de tareas para borrar
                page_token = tasks_result.get("nextPageToken")
                if not page_token:
                    break # Si no hay más páginas, salimos del bucle
            # ===== FIN DEL CÓDIGO CORREGIDO =====
            
            print("Lista limpiada.")

        if not tasklist_id:
            print("No se encontró ID o la lista no es válida. Creando una nueva...")
            tasklist_body = {"title": "🛒 Lista de Compras - DietFlow"}
            tasklist = service.tasklists().insert(body=tasklist_body).execute()
            tasklist_id = tasklist.get("id")
            
            if not config_entry:
                config_entry = Configuracion(clave="tasklist_id", valor=tasklist_id)
                db.add(config_entry)
            else:
                config_entry.valor = tasklist_id
            db.commit()
            print(f"Nueva lista creada con ID: {tasklist_id}. ID guardado en la base de datos.")

        print("Añadiendo nuevos ingredientes a la lista...")
        for nombre, data in shopping_list.items():
            task_body = {"title": f"{nombre} ({data['cantidad']} {data['unidad']})"}
            service.tasks().insert(tasklist=tasklist_id, body=task_body).execute()
        
        print("¡Lista de compras actualizada exitosamente!")
        return {"success": True, "tasklist_id": tasklist_id}
        
    except HttpError as err:
        if err.resp.status == 404:
            print("La lista guardada no fue encontrada en Google Tasks. Se creará una nueva.")
            if config_entry:
                db.delete(config_entry)
                db.commit()
            return update_or_create_shopping_list(db, shopping_list)
        else:
            print(err)
            return {"success": False, "error": str(err)}
        
if __name__ == "__main__":
    print("Intentando autenticar con Google Tasks para generar 'token.json'...")
    service = get_tasks_service()
    if service:
        print("\n¡Autenticación exitosa! 'token.json' ha sido creado.")
    else:
        print("\nFalló la autenticación.")