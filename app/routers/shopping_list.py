from fastapi import APIRouter, Depends, Form, BackgroundTasks
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import date
from typing import List

from database import get_db
from schemas.shopping_list import ShoppingListItemSchema
from services import shopping_list_service

from services import shopping_list_service, task_export_service
from repositories.config_repo import ConfigRepository
from google_client.client import GoogleTasksClient
from dependencies import get_google_client, get_config_repo


router = APIRouter(prefix="/lista-compras", tags=["Shopping List"])

@router.get(
    "/view-shopping-list", 
    response_model=List[ShoppingListItemSchema]  
)
def generate_shopping_list_data(dia_inicio: date, dia_fin: date, db: Session = Depends(get_db)):
    """
    Genera una lista de compras consolidada para un RANGO DE FECHAS
    y la devuelve en formato JSON.
    """
    return shopping_list_service.create_shopping_list_logic(
        db=db, 
        dia_inicio=dia_inicio, 
        dia_fin=dia_fin
    )

@router.post("/export-to-tasks")
def export_shopping_list_to_tasks(
    background_tasks: BackgroundTasks,
    ingredientes: List[str] = Form(...), # Así se reciben los datos de formulario
    db: Session = Depends(get_db),
    client: GoogleTasksClient = Depends(get_google_client),
    repo: ConfigRepository = Depends(get_config_repo)
):
    """
    Este endpoint toma los ingredientes de la lista de compras (ya calculados
    en el frontend o por otro endpoint) y los envía a Google Tasks.
    """
    # 1. Parsear los datos (lógica que estaba en process_and_send_tasks)
    shopping_list_dict = {}
    for item_str in ingredientes:
        try:
            nombre, cantidad, unidad = item_str.split('|')
            shopping_list_dict[nombre] = {"cantidad": float(cantidad), "unidad": unidad}
        except ValueError:
            continue
    
    if not shopping_list_dict:
        return RedirectResponse(url="/", status_code=303) # O algún error

    # 2. Encolar la tarea de exportación
    background_tasks.add_task(
        task_export_service.export_shopping_list,
        db=db,
        client=client,
        repo=repo,
        shopping_list=shopping_list_dict
    )
    
    # 3. Devolver una respuesta HTTP
    return RedirectResponse(url="/plan/hoy", status_code=303)