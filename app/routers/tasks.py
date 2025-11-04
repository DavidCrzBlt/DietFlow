from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from google_client.client import GoogleTasksClient
from services import task_export_service
from dependencies import get_google_client 
from database import get_db

router = APIRouter(prefix="/export-tasks", tags=["Google Tasks"])

@router.post("/daily-plan")
def export_daily_plan(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    client: GoogleTasksClient = Depends(get_google_client)
):
    """Exporta el plan de comidas de HOY a Google Tasks."""
    background_tasks.add_task(task_export_service.export_daily_plan, db, client)
    return {"message": "La exportación del plan diario ha comenzado."}

@router.post("/weekly-plan")
def export_weekly_plan(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    client: GoogleTasksClient = Depends(get_google_client)
):
    """Exporta el plan de comidas de TODA la semana a Google Tasks."""
    background_tasks.add_task(task_export_service.export_weekly_plan, db, client)
    return {"message": "La exportación del plan semanal ha comenzado."}