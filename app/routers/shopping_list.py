from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from typing import List

from database import get_db
from schemas.shopping_list import ShoppingListItemSchema
from services import shopping_list_service

router = APIRouter()

@router.get(
    "/lista-compras", 
    response_model=List[ShoppingListItemSchema]  
)
def generate_shopping_list_data(dia_inicio: date, dia_fin: date, db: Session = Depends(get_db)):
    """
    Genera una lista de compras consolidada para un RANGO DE FECHAS
    y la devuelve en formato JSON.
    """
    return shopping_list_service.get_shopping_list_logic(
        db=db, 
        dia_inicio=dia_inicio, 
        dia_fin=dia_fin
    )