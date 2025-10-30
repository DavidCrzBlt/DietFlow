# app/schemas.py
from pydantic import BaseModel
from typing import List

# --- Definimos las piezas más pequeñas primero ---

class IngredienteSchema(BaseModel):
    id: int
    nombre: str
    unidad: str

    class Config:
        orm_mode = True

class RecetaIngredienteSchema(BaseModel):
    cantidad: float
    ingrediente: IngredienteSchema

    class Config:
        orm_mode = True

class RecetaSchema(BaseModel):
    id: int
    nombre: str
    ingredientes: List[RecetaIngredienteSchema]

    class Config:
        orm_mode = True

# --- Definimos el objeto principal que enviaremos ---

class PlanComidaSchema(BaseModel):
    id: int
    momento_comida: str
    receta: RecetaSchema

    class Config:
        orm_mode = True

class PlanSemanalSchema(BaseModel):
    dia: str
    plan_comida: List[PlanComidaSchema]


class ShoppingListItemSchema(BaseModel):
    nombre: str
    cantidad: float
    unidad: str