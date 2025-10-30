import time
from datetime import datetime, timedelta, time as dt_time, date 
import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from sqlalchemy.orm import Session, joinedload
from models import SessionLocal, PlanSemanal, DiasEnum, Receta, RecetaIngrediente
from tasks_integration import get_tasks_service

TIMEZONE = "America/Mexico_City"

SCHEDULED_TIMES = {
    "desayuno": dt_time(8, 0),
    "refrigerio": dt_time(12, 0),
    "comida": dt_time(15, 0),
    "cena": dt_time(19, 0)
}

def plan_tomorrow_meals():
    print(f"[{datetime.now()}] - Iniciando planificador de comidas para mañana...")
    
    db = SessionLocal()
    service = get_tasks_service()

    if not service:
        print("Error: No se pudo conectar con el servicio de Google Tasks. Abortando.")
        db.close()
        return

    # ===== SOLUCIÓN PARA LA FECHA CORRECTA =====
    # Usamos un método más simple y robusto para evitar errores de zona horaria
    tomorrow_date = date.today() + timedelta(days=1)
    
    weekday_num = tomorrow_date.weekday()
    dias_map = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    dia_str = dias_map[weekday_num]
    dia_enum = DiasEnum[dia_str]

    plan_de_mañana = db.query(PlanSemanal).filter(PlanSemanal.dia == dia_enum).options(
        joinedload(PlanSemanal.receta)
        .joinedload(Receta.ingredientes)
        .joinedload(RecetaIngrediente.ingrediente)
    ).all()
    
    meal_order = ["desayuno", "refrigerio", "comida", "cena"]
    plan_de_mañana.sort(key=lambda plan: meal_order.index(plan.momento_comida.name))

    if not plan_de_mañana:
        print(f"No hay comidas planificadas para mañana ({dia_str}). Tarea finalizada.")
        db.close()
        return

    try:
        tasklists = service.tasklists().list().execute().get("items", [])
        for tl in tasklists:
            if tl['title'].startswith("🥗 Plan de Comida"):
                service.tasklists().delete(tasklist=tl['id']).execute()

        fecha_mañana_str = tomorrow_date.strftime("%A, %d de %B").capitalize()
        tasklist_body = {"title": f"🥗 Plan de Comida - {fecha_mañana_str}"}
        tasklist = service.tasklists().insert(body=tasklist_body).execute()
        tasklist_id = tasklist.get("id")
        print(f"Nueva lista creada: {tasklist_body['title']}")

        for plan in plan_de_mañana:
            task_title = f"{plan.momento_comida.value}: {plan.receta.nombre}"
            task_body = {"title": task_title}
            
            # ===== SOLUCIÓN PARA LA HORA CORRECTA =====
            meal_time = SCHEDULED_TIMES.get(plan.momento_comida.name)
            if meal_time:
                local_tz = pytz.timezone(TIMEZONE)
                naive_datetime = datetime.combine(tomorrow_date, meal_time)
                local_datetime = local_tz.localize(naive_datetime)
                utc_datetime = local_datetime.astimezone(pytz.utc)
                # Forzamos el formato exacto que Google espera, terminando en 'Z'
                task_body["due"] = utc_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')

            notes = "Ingredientes:\n"
            for item in plan.receta.ingredientes:
                notes += f"- {item.ingrediente.nombre} ({item.cantidad} {item.ingrediente.unidad.value})\n"
            task_body["notes"] = notes
            
            service.tasks().insert(tasklist=tasklist_id, body=task_body).execute()
            print(f"  - Tarea añadida: {task_title} (Recordatorio a las {meal_time})")

        print("¡Plan de mañana enviado a Google Tasks exitosamente!")

    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone=TIMEZONE)
    scheduler.add_job(plan_tomorrow_meals, 'cron', hour=3, minute=0)
    print("Ejecutando el planificador por primera vez al iniciar...")
    plan_tomorrow_meals()
    print("\nScheduler iniciado...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass