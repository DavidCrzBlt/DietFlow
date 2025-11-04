from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from models.plan import PlanSemanal, DiasEnum, Receta, RecetaIngrediente
from config import settings
from collections import defaultdict 


def get_daily_plan_logic(db: Session):
    weekday_num = datetime.now(settings.TZ).weekday()
    dias_map = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    dia_actual_str = dias_map[weekday_num]
    
    try:
        dia_actual_enum = DiasEnum[dia_actual_str]
    except KeyError:
        return f"Día {dia_actual_str} no encontrado"


    plan_del_dia = db.query(PlanSemanal).filter(
        PlanSemanal.dia == dia_actual_enum
    ).options(
        joinedload(PlanSemanal.receta)
        .joinedload(Receta.ingredientes)
        .joinedload(RecetaIngrediente.ingrediente)
    ).all()

    meal_order = ["desayuno", "refrigerio", "comida", "cena"]
    plan_del_dia.sort(key=lambda p: meal_order.index(p.momento_comida.name))

    return plan_del_dia



def get_weekly_plan_logic(db: Session):
    """
    Obtiene todo el plan semanal y lo agrupa por día.
    """
    plan_semanal_completo = db.query(PlanSemanal).options(
        joinedload(PlanSemanal.receta)
        .joinedload(Receta.ingredientes)
        .joinedload(RecetaIngrediente.ingrediente)
    ).all()

    plan_agrupado = defaultdict(list)
    for plan in plan_semanal_completo:
        plan_agrupado[plan.dia.name].append(plan) 

    meal_order = ["desayuno", "refrigerio", "comida", "cena"]
    for dia in plan_agrupado:
        plan_agrupado[dia].sort(key=lambda p: meal_order.index(p.momento_comida.name))
        
    return plan_agrupado