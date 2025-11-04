from fastapi import APIRouter, Depends, Form, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from services.google_task_service import process_and_send_tasks, send_weekly_plan_to_tasks


router = APIRouter()

@router.post("/send-to-tasks")
async def send_to_tasks_endpoint(
    background_tasks: BackgroundTasks,
    ingredientes: List[str] = Form(...),
    db: Session = Depends(get_db)
):
    """
    Este endpoint recibe la petición y la delega inmediatamente al servicio
    para que procese la lista y la envíe a Google Tasks.
    """
    return process_and_send_tasks(
        ingredientes=ingredientes, 
        db=db, 
        background_tasks=background_tasks
    )


@router.post("/plan-to-tasks")
def send_plan_to_tasks(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Envía el plan de comidas de TODA LA SEMANA a Google Tasks.
    """

    background_tasks.add_task(send_weekly_plan_to_tasks, db)
    return {"message": "El plan semanal se está enviando a Google Tasks."}