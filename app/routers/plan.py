from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services import plan_service
from utils import date_helpers
from config import settings
from datetime import datetime
from typing import List, Dict
from schemas import plan as plan_schema
from database import get_db 


router = APIRouter(
    prefix="/plan",
    tags=["Plan de Comidas"]
)

@router.get("/hoy", response_model=List[plan_schema.PlanComidaSchema])
def get_todays_plan(db: Session = Depends(get_db)):
    """
    Obtiene el plan de comidas (desayuno, comida, etc.) para el día actual.
    """
    today_info = date_helpers.get_day_info(datetime.now(settings.TZ).date())
    
    return plan_service.get_plan_for_day(db, dia=today_info.dia_enum)


@router.get("/semanal", response_model=Dict[str, List[plan_schema.PlanComidaSchema]])
def get_weekly_plan(db: Session = Depends(get_db)):
    """
    Devuelve el plan de comidas de toda la semana, agrupado por día (str).
    """

    return plan_service.get_plan_for_week_grouped(db)