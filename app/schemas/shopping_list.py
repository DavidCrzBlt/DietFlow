from pydantic import BaseModel

class ShoppingListItemSchema(BaseModel):
    nombre: str
    cantidad: float
    unidad: str