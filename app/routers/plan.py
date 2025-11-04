# app/routers/plan.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict
from database import get_db
from schemas import plan as plan_schema
from services import plan_service


router = APIRouter()

@router.get("/", response_model=List[plan_schema.PlanComidaSchema])
def get_todays_plan_data(db: Session = Depends(get_db)):

    return plan_service.get_daily_plan_logic(db)


@router.get("/plan/semana", response_model=Dict[str, List[plan_schema.PlanComidaSchema]])
def get_weekly_plan_data(db: Session = Depends(get_db)):
    """
    Devuelve el plan de comidas de toda la semana, agrupado por día.
    """
    return plan_service.get_weekly_plan_logic(db)