import locale
from datetime import datetime, timedelta, date
from collections import defaultdict
from fastapi import FastAPI, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi import Form
from typing import List
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from models import Base, engine, SessionLocal, PlanSemanal, DiasEnum, Receta, RecetaIngrediente
from tasks_integration import create_shopping_list_task

# Establecer el locale en español para obtener el nombre del día correctamente
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_TIME, 'Spanish')


# --- Configuración de la App y Base de Datos ---
Base.metadata.create_all(bind=engine)
app = FastAPI(title="DietFlow")

# Configura el motor de plantillas Jinja2
templates = Jinja2Templates(directory="templates")

# --- Dependencia para la Sesión de Base de Datos ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpoints de la API ---

@app.get("/")
def get_todays_plan_view(request: Request, db: Session = Depends(get_db)):
    """
    Obtiene el plan de comidas para el día actual y lo muestra en una vista HTML.
    """

    weekday_num = datetime.now().weekday()

    # 2. Mapear el número al string de nuestro Enum (la clave, no el valor)
    
    dias_map = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    dia_actual_str = dias_map[weekday_num]

    try:
        # Convertir el string del día al miembro del Enum correspondiente
        dia_actual_enum = DiasEnum[dia_actual_str]
    except KeyError:
        # Si el día no existe en el Enum (no debería pasar), devolver un error o página vacía
        return templates.TemplateResponse("index.html", {
            "request": request,
            "dia_actual": "Día no encontrado",
            "plan_del_dia": []
        })

    # 2. Consultar la base de datos para el plan de hoy
    plan_del_dia = db.query(PlanSemanal).filter(PlanSemanal.dia == dia_actual_enum)\
        .options(
            joinedload(PlanSemanal.receta)
            .joinedload(Receta.ingredientes)
            .joinedload(RecetaIngrediente.ingrediente)
        ).all()

    # 3. Renderizar la plantilla HTML con los datos
    return templates.TemplateResponse("index.html", {
        "request": request,
        "dia_actual": dia_actual_str,
        "plan_del_dia": plan_del_dia,
        "dias_enum": DiasEnum
    })


@app.get("/lista-compras")
def generate_shopping_list(request: Request, dia_inicio: date, dia_fin: date, db: Session = Depends(get_db)):
    """
    Genera una lista de compras consolidada para un RANGO DE FECHAS específico.
    FastAPI convierte automáticamente los strings "YYYY-MM-DD" del formulario a objetos 'date'.
    """
    if dia_inicio > dia_fin:
        return {"error": "La fecha de inicio no puede ser posterior a la fecha de fin."}

    # El "truquito" para sumar ingredientes
    lista_compras = defaultdict(lambda: {'cantidad': 0, 'unidad': ''})
    dias_map = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    
    # 1. Bucle a través de cada día en el rango de fechas seleccionado
    delta = dia_fin - dia_inicio
    for i in range(delta.days + 1):
        current_date = dia_inicio + timedelta(days=i)
        
        # 2. Averiguar qué día de la semana es (Lunes=0, etc.)
        weekday_num = current_date.weekday()
        dia_str = dias_map[weekday_num]
        dia_enum = DiasEnum[dia_str]
        
        # 3. Buscar las comidas para ESE día de la semana
        planes_del_dia = db.query(PlanSemanal).filter(PlanSemanal.dia == dia_enum)\
            .options(
                joinedload(PlanSemanal.receta)
                .joinedload(Receta.ingredientes)
                .joinedload(RecetaIngrediente.ingrediente)
            ).all()
        
        # 4. Sumar los ingredientes de ese día a nuestra lista total
        for plan in planes_del_dia:
            for item in plan.receta.ingredientes:
                nombre = item.ingrediente.nombre
                lista_compras[nombre]['cantidad'] += item.cantidad
                lista_compras[nombre]['unidad'] = item.ingrediente.unidad.value

    # 5. Renderizar la plantilla con la lista final
    return templates.TemplateResponse("lista_compras.html", {
        "request": request,
        "lista_compras": dict(lista_compras),
        "dia_inicio": dia_inicio,
        "dia_fin": dia_fin
    })

@app.post("/send-to-tasks")
async def send_list_to_tasks(ingredientes: List[str] = Form(...)):
    """
    Recibe la lista de ingredientes directamente desde el formulario
    y crea la nota en Google Tasks.
    """
    shopping_list = {}
    for item_str in ingredientes:
        # Usamos try-except por si algún dato viene malformado
        try:
            nombre, cantidad, unidad = item_str.split('|')
            shopping_list[nombre] = {
                "cantidad": float(cantidad),
                "unidad": unidad
            }
        except ValueError:
            # Ignora este ingrediente si no tiene el formato correcto
            continue
    
    # El resto de la función no cambia
    if shopping_list: # Solo crea la nota si tenemos ingredientes
        resultado = create_shopping_list_task(shopping_list)
    
    return RedirectResponse(url="/", status_code=303)