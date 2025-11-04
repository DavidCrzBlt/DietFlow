import os.path
from fastapi import BackgroundTasks
from fastapi.responses import RedirectResponse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from sqlalchemy.orm import Session, joinedload
from models.plan import Configuracion, PlanSemanal, Receta, RecetaIngrediente, DiasEnum
from typing import List
from datetime import datetime, timedelta, date
from config import settings
from services import plan_service
from zoneinfo import ZoneInfo

# El único cambio de configuración: el permiso que pedimos ahora es para Tasks.
SCOPES = ["https://www.googleapis.com/auth/tasks"]

def get_tasks_service():
    """Autentica y crea un objeto de servicio para interactuar con la API de Tasks."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("tasks", "v1", credentials=creds)
        return service
    except HttpError as err:
        print(err)
        return None

def update_or_create_shopping_list(db: Session, shopping_list: dict):
    """
    Busca la lista de compras de DietFlow, la limpia y la actualiza.
    Si no existe, la crea y guarda su ID.
    """
    service = get_tasks_service()
    if not service:
        return {"error": "No se pudo conectar con el servicio de Tasks."}

    config_entry = db.query(Configuracion).filter(Configuracion.clave == "tasklist_id").first()
    tasklist_id = config_entry.valor if config_entry else None

    try:
        if tasklist_id:
            print(f"Encontrado ID de lista: {tasklist_id}. Limpiando tareas existentes...")  

            page_token = None
            while True:
                tasks_result = service.tasks().list(
                    tasklist=tasklist_id,
                    pageToken=page_token
                ).execute()

                tasks = tasks_result.get("items", [])
                for task in tasks:
                    service.tasks().delete(tasklist=tasklist_id, task=task.get("id")).execute()

                page_token = tasks_result.get("nextPageToken")
                if not page_token:
                    break 

            print("Lista limpiada.")

        if not tasklist_id:
            print("No se encontró ID o la lista no es válida. Creando una nueva...")
            tasklist_body = {"title": "🛒 Lista de Compras - DietFlow"}
            tasklist = service.tasklists().insert(body=tasklist_body).execute()
            tasklist_id = tasklist.get("id")

            if not config_entry:
                config_entry = Configuracion(clave="tasklist_id", valor=tasklist_id)
                db.add(config_entry)
            else:
                config_entry.valor = tasklist_id
            db.commit()
            print(f"Nueva lista creada con ID: {tasklist_id}. ID guardado en la base de datos.")

        print("Añadiendo nuevos ingredientes a la lista...")
        for nombre, data in shopping_list.items():
            task_body = {"title": f"{nombre} ({data['cantidad']} {data['unidad']})"}
            service.tasks().insert(tasklist=tasklist_id, body=task_body).execute()

        print("¡Lista de compras actualizada exitosamente!")
        return {"success": True, "tasklist_id": tasklist_id}

    except HttpError as err:
        if err.resp.status == 404:
            print("La lista guardada no fue encontrada en Google Tasks. Se creará una nueva.")
            if config_entry:
                db.delete(config_entry)
                db.commit()
            return update_or_create_shopping_list(db, shopping_list)
        else:
            print(err)
            return {"success": False, "error": str(err)}
        

def process_and_send_tasks(
    ingredientes: List[str], 
    db: Session, 
    background_tasks: BackgroundTasks
):
    """
    Esta es la lógica de negocio que antes estaba en el endpoint.
    Procesa los ingredientes y añade la actualización a las tareas en segundo plano.
    """
    shopping_list = {}
    for item_str in ingredientes:
        try:
            nombre, cantidad, unidad = item_str.split('|')
            shopping_list[nombre] = {"cantidad": float(cantidad), "unidad": unidad}
        except ValueError:
            continue
    
    if shopping_list:
        background_tasks.add_task(update_or_create_shopping_list, db, shopping_list)
    
    return RedirectResponse(url="/", status_code=303)


def create_daily_plan_on_tasks(db: Session):
    """
    Toma la lógica de 'plan_tomorrow_meals' y la convierte en un servicio.
    Obtiene el plan de HOY y lo envía a Google Tasks con recordatorios.
    """
    service = get_tasks_service()
    if not service:
        print("Error: No se pudo conectar con el servicio de Google Tasks.")
        return {"success": False, "error": "No se pudo conectar a Google Tasks"}

    try:
        today_date = datetime.now(settings.TZ).date()
        
        weekday_num = today_date.weekday()
        dias_map = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
        dia_str = dias_map[weekday_num]
        
        dia_enum = DiasEnum[dia_str]

        plan_de_hoy = db.query(PlanSemanal).filter(PlanSemanal.dia == dia_enum).options(
            joinedload(PlanSemanal.receta)
            .joinedload(Receta.ingredientes)
            .joinedload(RecetaIngrediente.ingrediente)
        ).all()

        if not plan_de_hoy:
            return {"success": False, "error": f"No hay comidas planificadas para hoy ({dia_str})."}
        
        meal_order = ["desayuno", "refrigerio", "comida", "cena"]
        plan_de_hoy.sort(key=lambda p: meal_order.index(p.momento_comida.name))

        tasklists = service.tasklists().list().execute().get("items", [])
        for tl in tasklists:
            if tl['title'].startswith("🥗 Plan de Comida"):
                service.tasklists().delete(tasklist=tl['id']).execute()

        fecha_str = today_date.strftime("%A, %d de %B").capitalize()
        tasklist_body = {"title": f"🥗 Plan de Comida - {fecha_str}"}
        tasklist = service.tasklists().insert(body=tasklist_body).execute()
        tasklist_id = tasklist.get("id")

        for plan in plan_de_hoy:
            task_title = f"{plan.momento_comida.value}: {plan.receta.nombre}"
            task_body = {"title": task_title}
            
            task_body["due"] = today_date.isoformat() + "T00:00:00Z"

            notes = "Ingredientes:\n"
            for item in plan.receta.ingredientes:
                notes += f"- {item.ingrediente.nombre} ({item.cantidad} {item.ingrediente.unidad.value})\n"
            task_body["notes"] = notes
            
            service.tasks().insert(tasklist=tasklist_id, body=task_body).execute()
        
        return {"success": True, "message": f"Plan para {fecha_str} enviado a Tasks."}

    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return {"success": False, "error": str(e)}
    
def send_weekly_plan_to_tasks(db: Session):
    service = get_tasks_service()
    if not service:
        print("Error: No se pudo conectar con Google Tasks.")
        return {"success": False, "error": "No se pudo conectar a Google Tasks"}

    print(f"[{datetime.now()}] Iniciando envío del plan semanal completo a Tasks...")

    try:
        plan_agrupado = plan_service.get_weekly_plan_logic(db)
        if not plan_agrupado:
            print("No se encontró plan semanal en la base de datos.")
            return {"success": False, "error": "No se encontró plan semanal."}

        print("Limpiando listas de planes antiguos...")
        tasklists = service.tasklists().list().execute().get("items", [])
        for tl in tasklists:
            if tl['title'].startswith("🥗 Plan"):
                service.tasklists().delete(tasklist=tl['id']).execute()

        # --- INICIO DE LA NUEVA LÓGICA DE FECHAS ---
        # 1. Obtenemos la fecha de "hoy" en nuestra zona horaria
        today = datetime.now(settings.TZ).date()
        
        # 2. Calculamos qué día fue el lunes de esta semana
        # (today.weekday() da Lunes=0, Martes=1...)
        start_of_week = today - timedelta(days=today.weekday())
        
        dias_map = {"lunes": 0, "martes": 1, "miercoles": 2, "jueves": 3, "viernes": 4, "sabado": 5, "domingo": 6}

        for dia in dias_map.keys():
            plan_del_dia = plan_agrupado.get(dia)
            
            if not plan_del_dia:
                continue 

            dia_titulo = dia.capitalize()
            tasklist_body = {"title": f"🥗 Plan - {dia_titulo}"}
            tasklist = service.tasklists().insert(body=tasklist_body).execute()
            tasklist_id = tasklist.get("id")
            print(f"Lista creada: {tasklist_body['title']}")

            # 3. Calculamos la fecha para las tareas de este día
            offset = dias_map[dia]
            task_date = start_of_week + timedelta(days=offset)
            # Formato UTC que Google espera (como "todo el día")
            due_date_str = task_date.isoformat() + "T00:00:00Z"

            for plan in plan_del_dia:
                task_title = f"{plan.momento_comida.value}: {plan.receta.nombre}"
                task_body = {
                    "title": task_title,
                    "due": due_date_str  
                }
                
                notes = "Ingredientes:\n"
                for item in plan.receta.ingredientes:
                    notes += f"- {item.ingrediente.nombre} ({item.cantidad} {item.ingrediente.unidad.value})\n"
                task_body["notes"] = notes
                
                service.tasks().insert(tasklist=tasklist_id, body=task_body).execute()

        print("¡Plan semanal completo enviado a Google Tasks!")
        return {"success": True, "message": "Plan semanal enviado a Tasks."}

    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return {"success": False, "error": str(e)}