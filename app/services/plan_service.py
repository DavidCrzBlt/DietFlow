from sqlalchemy.orm import Session, joinedload
from models.plan import PlanSemanal, DiasEnum, Receta, RecetaIngrediente, TipoComidaEnum
from collections import defaultdict 
from typing import List, Dict


MEAL_ORDER_LIST = [
    TipoComidaEnum.desayuno, 
    TipoComidaEnum.refrigerio, 
    TipoComidaEnum.comida, 
    TipoComidaEnum.cena
]


def _get_base_plan_query(db: Session):
    """
    Helper privado que crea la consulta base con todos los 'joinedloads'.
    No se repite más.
    """
    return db.query(PlanSemanal).options(
        joinedload(PlanSemanal.receta)
        .joinedload(Receta.ingredientes)
        .joinedload(RecetaIngrediente.ingrediente)
    )

def _sort_plan_by_mealtime(plan_list: List[PlanSemanal]) -> List[PlanSemanal]:
    """
    Helper privado que ordena una lista de planes por el momento de comida.
    """
    # Usamos .get() para evitar errores si un nombre no está en la lista
    meal_order_dict = {name: i for i, name in enumerate(MEAL_ORDER_LIST)}
    
    plan_list.sort(key=lambda p: meal_order_dict.get(p.momento_comida.name, 99))
    return plan_list

# --- 2. Lógica de Servicio Pública (APIs del servicio) ---

def get_plan_for_day(db: Session, dia: DiasEnum) -> List[PlanSemanal]:
    """
    Obtiene el plan completo para un DÍA ESPECÍFICO.
    Ya no calcula 'hoy', solo obedece.
    """
    plan_del_dia = _get_base_plan_query(db).filter(
        PlanSemanal.dia == dia
    ).all()
    
    return _sort_plan_by_mealtime(plan_del_dia)


def get_plan_for_week_grouped(db: Session) -> Dict[str, List[PlanSemanal]]:
    """
    Obtiene todo el plan semanal y lo agrupa por día, ya ordenado.
    """
    plan_semanal_completo = _get_base_plan_query(db).all()

    plan_agrupado = defaultdict(list)
    for plan in plan_semanal_completo:
        plan_agrupado[plan.dia.name].append(plan) 

    # Ordenamos la lista de cada día
    for dia_str, plan_list in plan_agrupado.items():
        plan_agrupado[dia_str] = _sort_plan_by_mealtime(plan_list)
        
    return plan_agrupado


def get_plan_for_days_list(db: Session, dias: List[DiasEnum]) -> List[PlanSemanal]:
    """
    Obtiene un listado PLANO de todos los planes para una lista de enums de días.
    Esta es la consulta única que necesitamos para la lista de compras.
    """
    if not dias:
        return []
        
    # Reutilizamos el helper que ya habíamos creado
    return _get_base_plan_query(db).filter(
        PlanSemanal.dia.in_(dias)
    ).all()