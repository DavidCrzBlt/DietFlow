# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import plan, shopping_list, tasks

# models.Base.metadata.create_all(bind=engine) # Esto puede ir aquí o en database.py

app = FastAPI(title="DietFlow")

# Configuración de CORS
origins = ["http://localhost:5173", "http://localhost"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluimos los routers de nuestras "habitaciones"
app.include_router(plan.router)
app.include_router(shopping_list.router)
app.include_router(tasks.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a DietFlow API"}



