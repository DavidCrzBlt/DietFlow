import locale
from datetime import datetime
from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from models import Base, engine, SessionLocal, PlanSemanal, DiasEnum, Receta, RecetaIngrediente

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
        "plan_del_dia": plan_del_dia
    })