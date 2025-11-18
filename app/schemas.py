# app/schemas.py

from pydantic import BaseModel
from typing import List
from datetime import datetime

# --- Esquemas para Option (Opción de Voto) ---

# Esquema base (lo que tienen en común)
class OptionBase(BaseModel):
    option_text: str

# Esquema para *crear* una opción (solo necesita el texto)
class OptionCreate(OptionBase):
    pass

# Esquema para *mostrar* una opción (devuelve todo, incl. el ID y votos)
class Option(OptionBase):
    id: int
    poll_id: int
    vote_count: int

    # Configuración para que Pydantic entienda los modelos de SQLAlchemy
    # (Esta es la sintaxis "clásica" para Pydantic v1)
    class Config:
        orm_mode = True


# --- Esquemas para Poll (Encuesta) ---

# Esquema base
class PollBase(BaseModel):
    question_text: str

# Esquema para *crear* una encuesta
class PollCreate(PollBase):
    # Espera una lista de objetos que sigan la forma de OptionCreate
    # ej: [{"option_text": "Sí"}, {"option_text": "No"}]
    options: List[OptionCreate]

# Esquema para *mostrar* una encuesta
class Poll(PollBase):
    id: int
    created_at: datetime
    options: List[Option] = [] # Muestra la lista de opciones
    
    # Configuración para que Pydantic entienda los modelos de SQLAlchemy
    class Config:
        orm_mode = True