from datetime import date
from models.plan import DiasEnum

# Definimos las constantes una sola vez para ser reutilizadas
DIAS_SEMANA_LIST = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
DIAS_SEMANA_DICT = {dia: i for i, dia in enumerate(DIAS_SEMANA_LIST)}

class DayInfo(object):
    """Una clase simple para devolver la información del día de forma estructurada."""
    def __init__(self, dia_str: str, dia_enum: DiasEnum):
        self.dia_str = dia_str
        self.dia_enum = dia_enum

def get_day_info(target_date: date) -> DayInfo:
    """
    A partir de una fecha, devuelve el nombre del día y su valor Enum correspondiente.
    """
    weekday_num = target_date.weekday()  # Lunes=0, Martes=1, etc.
    dia_str = DIAS_SEMANA_LIST[weekday_num]
    dia_enum = DiasEnum[dia_str]
    return DayInfo(dia_str=dia_str, dia_enum=dia_enum)
