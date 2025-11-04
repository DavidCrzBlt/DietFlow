from sqlalchemy.orm import Session
from datetime import date, timedelta
from collections import defaultdict
from typing import List, Dict, Any


from utils import date_helpers
from services import plan_service

def create_shopping_list_logic(dia_inicio: date, dia_fin: date, db: Session) -> List[Dict[str, Any]]:
    """
    Genera una lista de compras consolidada para un RANGO DE FECHAS.
    """
    if dia_inicio > dia_fin:
        # Es mejor devolver un error o un diccionario con error
        # Pero para mantener tu lógica, devolvemos lista vacía
        return [] 
        # o: return {"error": "La fecha de inicio no puede ser posterior a la fecha de fin."}


    dias_a_consultar = set()
    delta_dias = (dia_fin - dia_inicio).days
    
    for i in range(delta_dias + 1):
        current_date = dia_inicio + timedelta(days=i)
        day_info = date_helpers.get_day_info(current_date)
        dias_a_consultar.add(day_info.dia_enum)

    if not dias_a_consultar:
        return [] 
    
    planes_del_rango = plan_service.get_plan_for_days_list(db, list(dias_a_consultar))
    
    lista_compras = defaultdict(lambda: {'cantidad': 0, 'unidad': ''})
    
    for pl in planes_del_rango:
        for item in pl.receta.ingredientes:
            nombre_ingrediente = item.ingrediente.nombre
            lista_compras[nombre_ingrediente]['cantidad'] += item.cantidad
            lista_compras[nombre_ingrediente]['unidad'] = item.ingrediente.unidad.value

    response_list = [
        {"nombre": nombre, "cantidad": data['cantidad'], "unidad": data['unidad']}
        for nombre, data in lista_compras.items()
    ]

    return response_list