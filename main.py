from fastapi import FastAPI
from models import Base, engine

Base.metadata.create_all(bind=engine)


app = FastAPI(title="DietFlow API")

@app.get("/")
def read_root():
    """
    Endpoint de bienvenida para verificar que el servidor está funcionando.
    """
    return {"message": "¡Bienvenido a DietFlow! El esqueleto del proyecto está listo."}