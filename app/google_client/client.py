from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from typing import List


class GoogleTasksClient:
    """
    Un cliente "tonto" que solo sabe cómo hablar con la API de Google Tasks.
    No sabe nada de la lógica de DietFlow.
    """
    service: Resource # Type hint para el servicio

    def __init__(self, creds: Credentials):
        if not creds:
            raise ConnectionError("No se pueden construir el cliente sin credenciales.")
        try:
            self.service = build("tasks", "v1", credentials=creds)
        except HttpError as e:
            raise ConnectionError(f"No se pudo construir el servicio de Google: {e}")

    def clear_tasklist(self, tasklist_id: str):
        """Elimina todas las tareas dentro de una lista."""
        page_token = None
        while True:
            tasks_result = self.service.tasks().list(
                tasklist=tasklist_id, pageToken=page_token
            ).execute()
            
            for task in tasks_result.get("items", []):
                self.service.tasks().delete(
                    tasklist=tasklist_id, task=task.get("id")
                ).execute()
            
            page_token = tasks_result.get("nextPageToken")
            if not page_token:
                break
        print(f"Cliente: Lista {tasklist_id} limpiada.")

    def find_tasklists_by_prefix(self, prefix: str) -> List[dict]:
        """Encuentra listas de tareas que comiencen con un prefijo."""
        all_tasklists = self.service.tasklists().list().execute().get("items", [])
        return [tl for tl in all_tasklists if tl.get('title', '').startswith(prefix)]

    def delete_tasklist(self, tasklist_id: str):
        """Elimina una lista de tareas por su ID."""
        self.service.tasklists().delete(tasklist=tasklist_id).execute()
        print(f"Cliente: Lista {tasklist_id} eliminada.")

    def create_tasklist(self, title: str) -> dict:
        """Crea una nueva lista de tareas y la devuelve."""
        tasklist_body = {"title": title}
        return self.service.tasklists().insert(body=tasklist_body).execute()

    def create_task(self, tasklist_id: str, title: str, notes: str = None, due: str = None):
        """Crea una nueva tarea."""
        task_body = {"title": title}
        if notes:
            task_body["notes"] = notes
        if due:
            task_body["due"] = due # Formato "YYYY-MM-DDTHH:MM:SSZ"
        
        self.service.tasks().insert(tasklist=tasklist_id, body=task_body).execute()