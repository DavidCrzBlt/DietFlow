from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum


# Clases

class TipoComidaEnum(enum.Enum):
    desayuno = "Desayuno"
    refrigerio = "Refrigerio"
    comida = "Comida"
    cena = "Cena"

class UnidadEnum(enum.Enum):
    piezas = "piezas"
    gramos = "gramos"
    taza = "taza"
    cucharada = "cucharada"
    mililitros = "ml"
    sobre = "sobre"
    lata = "lata"

class DiasEnum(enum.Enum):
    lunes = "Lunes"
    martes = "Martes"
    miercoles = "Miércoles"
    jueves = "Jueves"
    viernes = "Viernes"
    sabado = "Sábado"
    domingo = "Domingo"

class Receta(Base):
    __tablename__ = "recetas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    tipo_comida = Column(Enum(TipoComidaEnum))
    instrucciones = Column(String, nullable=True)
    
    # Relaciones
    ingredientes = relationship("RecetaIngrediente", back_populates="receta")

class Ingrediente(Base):
    __tablename__ = "ingredientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    unidad = Column(Enum(UnidadEnum))

    # Relaciones
    recetas = relationship("RecetaIngrediente", back_populates="ingrediente")

class RecetaIngrediente(Base):
    __tablename__ = "receta_ingredientes"
    receta_id = Column(Integer, ForeignKey("recetas.id"), primary_key=True)
    ingrediente_id = Column(Integer, ForeignKey("ingredientes.id"), primary_key=True)
    cantidad = Column(Float)
    
    # Relaciones
    receta = relationship("Receta", back_populates="ingredientes")
    ingrediente = relationship("Ingrediente", back_populates="recetas")

class PlanSemanal(Base):
    __tablename__ = "plan_semanal"
    id = Column(Integer, primary_key=True, index=True)
    dia = Column(Enum(DiasEnum), index=True)
    momento_comida = Column(Enum(TipoComidaEnum))
    receta_id = Column(Integer, ForeignKey("recetas.id"))

    # Relación
    receta = relationship("Receta")

class Configuracion(Base):
    __tablename__ = "configuracion"
    id = Column(Integer, primary_key=True, index=True)
    clave = Column(String, unique=True, index=True) 
    valor = Column(String) 