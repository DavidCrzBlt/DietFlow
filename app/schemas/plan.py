from pydantic import BaseModel, ConfigDict
from typing import List
from pydantic import BaseModel, ConfigDict
from typing import List

class IngredienteSchema(BaseModel):
    # En lugar de la clase Config, usamos esto:
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    unidad: str

class RecetaIngredienteSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cantidad: float
    ingrediente: IngredienteSchema

class RecetaSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    ingredientes: List[RecetaIngredienteSchema]

class PlanComidaSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    momento_comida: str # Asegúrate de que esto coincida con el tipo en tu modelo (Enum o str)
    receta: RecetaSchema

class PlanSemanalSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    dia: str # Asegúrate de que esto coincida con el tipo en tu modelo (Enum o str)
    plan_comida: List[PlanComidaSchema]