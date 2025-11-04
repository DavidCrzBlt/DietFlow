from sqlalchemy.orm import Session
from google_client.client import GoogleTasksClient
from repositories.config_repo import ConfigRepository
from services import plan_service 
from utils import date_helpers
from models.plan import DiasEnum
from datetime import datetime, timedelta
from config import settings
from googleapiclient.errors import HttpError

# --- Constantes de Lógica de Negocio ---
SHOPPING_LIST_TITLE = "🛒 Lista de Compras - DietFlow"
DAILY_PLAN_PREFIX = "🥗 Plan de Comida"
WEEKLY_PLAN_PREFIX = "🥗 Plan"

def format_recipe_notes(receta) -> str:
    """Helper para crear la nota de ingredientes."""
    notes = "Ingredientes:\n"
    for item in receta.ingredientes:
        notes += f"- {item.ingrediente.nombre} ({item.cantidad} {item.ingrediente.unidad.value})\n"
    return notes

def export_shopping_list(
    db: Session, 
    client: GoogleTasksClient, 
    repo: ConfigRepository, 
    shopping_list: dict
):
    """
    Toma un diccionario de lista de compras y lo envía a Google Tasks.
    """
    tasklist_id = repo.get_shopping_list_task_id()

    try:
        if tasklist_id:
            print(f"Limpiando lista de compras existente: {tasklist_id}")
            client.clear_tasklist(tasklist_id)
        
        if not tasklist_id:
            print("Creando nueva lista de compras...")
            tasklist = client.create_tasklist(SHOPPING_LIST_TITLE)
            tasklist_id = tasklist.get("id")
            repo.save_shopping_list_task_id(tasklist_id)
        
        print("Añadiendo ingredientes a la lista...")
        for nombre, data in shopping_list.items():
            task_title = f"{nombre} ({data['cantidad']} {data['unidad']})"
            client.create_task(tasklist_id, title=task_title)
        
        db.commit()
        print("¡Lista de compras exportada con éxito!")
        return {"success": True, "tasklist_id": tasklist_id}

    except HttpError as err:
        if err.resp.status == 404 and tasklist_id:
            print("Lista no encontrada en Google. Borrando ID de la BD y reintentando.")
            db.delete(repo._get_config(repo.CONFIG_KEY_SHOPPING_LIST))
            db.commit()
            # Recursión segura para reintentar una vez
            return export_shopping_list(db, client, repo, shopping_list)
        
        db.rollback()
        print(f"Error HTTP: {err}")
        return {"success": False, "error": str(err)}
    except Exception as e:
        db.rollback()
        print(f"Error inesperado: {e}")
        return {"success": False, "error": str(e)}

def export_daily_plan(db: Session, client: GoogleTasksClient):
    """
    Obtiene el plan de HOY (usando plan_service) y lo envía a Tasks.
    """
    try:
        # 1. Obtener datos (usando helpers y servicios, no lógica aquí)
        today = datetime.now(settings.TZ).date()
        today_info = date_helpers.get_day_info(today)
        
        # ¡REUTILIZACIÓN! Llamamos al servicio que ya refactorizamos
        plan_de_hoy = plan_service.get_plan_for_day(db, today_info.dia_enum)

        if not plan_de_hoy:
            return {"success": False, "error": f"No hay plan para hoy ({today_info.dia_str})."}

        # 2. Interactuar con la API (usando el cliente)
        print("Limpiando planes diarios antiguos...")
        old_lists = client.find_tasklists_by_prefix(DAILY_PLAN_PREFIX)
        for tl in old_lists:
            client.delete_tasklist(tl['id'])

        fecha_str = today.strftime("%A, %d de %B").capitalize()
        tasklist_title = f"{DAILY_PLAN_PREFIX} - {fecha_str}"
        tasklist = client.create_tasklist(tasklist_title)
        tasklist_id = tasklist.get("id")
        
        due_date_str = today.isoformat() + "T00:00:00Z" # Tarea para todo el día

        for plan in plan_de_hoy:
            task_title = f"{plan.momento_comida.value}: {plan.receta.nombre}"
            notes = format_recipe_notes(plan.receta)
            client.create_task(tasklist_id, task_title, notes, due_date_str)
        
        return {"success": True, "message": f"Plan para {fecha_str} enviado."}

    except Exception as e:
        print(f"Error inesperado: {e}")
        return {"success": False, "error": str(e)}


def export_weekly_plan(db: Session, client: GoogleTasksClient):
    """
    Obtiene el plan SEMANAL (usando plan_service) y lo envía a Tasks.
    """
    try:
        # 1. Obtener datos (¡REUTILIZACIÓN!)
        plan_agrupado = plan_service.get_plan_for_week_grouped(db)
        if not plan_agrupado:
            return {"success": False, "error": "No se encontró plan semanal."}
        
        # 2. Interactuar con la API
        print("Limpiando planes semanales antiguos...")
        old_lists = client.find_tasklists_by_prefix(WEEKLY_PLAN_PREFIX)
        for tl in old_lists:
            client.delete_tasklist(tl['id'])

        today = datetime.now(settings.TZ).date()
        start_of_week = today - timedelta(days=today.weekday())

        # Usamos los helpers que ya creamos
        for dia_str in date_helpers.DIAS_SEMANA_LIST:
            plan_del_dia = plan_agrupado.get(dia_str)
            if not plan_del_dia:
                continue

            # Crear una lista para este día
            tasklist_title = f"{WEEKLY_PLAN_PREFIX} - {dia_str.capitalize()}"
            tasklist = client.create_tasklist(tasklist_title)
            tasklist_id = tasklist.get("id")
            
            # Calcular fecha de vencimiento
            offset = date_helpers.DIAS_SEMANA_DICT[dia_str]
            task_date = start_of_week + timedelta(days=offset)
            due_date_str = task_date.isoformat() + "T00:00:00Z"

            for plan in plan_del_dia:
                task_title = f"{plan.momento_comida.value}: {plan.receta.nombre}"
                notes = format_recipe_notes(plan.receta)
                client.create_task(tasklist_id, task_title, notes, due_date_str)
        
        return {"success": True, "message": "Plan semanal enviado a Tasks."}

    except Exception as e:
        print(f"Error inesperado: {e}")
        return {"success": False, "error": str(e)}