from sqlalchemy.orm import Session, joinedload
from datetime import date, timedelta
from collections import defaultdict
from models import plan


def create_shopping_list_logic(dia_inicio: date, dia_fin: date, db: Session):
    """
    Genera una lista de compras consolidada para un RANGO DE FECHAS específico.
    FastAPI convierte automáticamente los strings "YYYY-MM-DD" del formulario a objetos 'date'.
    """
    if dia_inicio > dia_fin:
        return {"error": "La fecha de inicio no puede ser posterior a la fecha de fin."}

    lista_compras = defaultdict(lambda: {'cantidad': 0, 'unidad': ''})
    dias_map = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    
    delta = dia_fin - dia_inicio
    for i in range(delta.days + 1):
        current_date = dia_inicio + timedelta(days=i)
        
        weekday_num = current_date.weekday()
        dia_str = dias_map[weekday_num]
        dia_enum = plan.DiasEnum[dia_str]
        
        planes_del_dia = db.query(plan.PlanSemanal).filter(plan.PlanSemanal.dia == dia_enum)\
            .options(
                joinedload(plan.PlanSemanal.receta)
                .joinedload(plan.Receta.ingredientes)
                .joinedload(plan.RecetaIngrediente.ingrediente)
            ).all()
        
        for pl in planes_del_dia:
            for item in plan.receta.ingredientes:
                nombre = item.ingrediente.nombre
                lista_compras[nombre]['cantidad'] += item.cantidad
                lista_compras[nombre]['unidad'] = item.ingrediente.unidad.value

        response_list = [
        {"nombre": nombre, "cantidad": data['cantidad'], "unidad": data['unidad']}
        for nombre, data in lista_compras.items()
    ]

    return response_list