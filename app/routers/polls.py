# app/routers/polls.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Importaciones locales
from .. import models, schemas
from ..database import get_db

# --- Configuración del Router ---
# Creamos un "mini-app" solo para las rutas de las encuestas.
router = APIRouter(
    prefix="/api",  # Todos los endpoints aquí empezarán con /api
    tags=["Polls"]  # Para agruparlos en la documentación /docs
)

# --- Endpoint 1: Crear una nueva encuesta ---
@router.post("/polls", 
             response_model=schemas.Poll, 
             status_code=status.HTTP_201_CREATED)
def create_poll(poll: schemas.PollCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva encuesta con sus opciones.
    """
    # 1. Crea el objeto Poll (Encuesta)
    db_poll = models.Poll(question_text=poll.question_text)
    
    # 2. Crea los objetos Option (Opción)
    db_options = [models.Option(option_text=opt.option_text) for opt in poll.options]
    
    # 3. Asocia las opciones con la encuesta
    db_poll.options = db_options

    # 4. Guarda todo en la base de datos
    db.add(db_poll)
    db.commit()
    
    # 5. Refresca el objeto para obtener los IDs generados por la BD
    db.refresh(db_poll)
    return db_poll

# --- Endpoint 2: Obtener todas las encuestas ---
@router.get("/polls", response_model=List[schemas.Poll])
def get_all_polls(db: Session = Depends(get_db)):
    """
    Retorna una lista de todas las encuestas con sus opciones.
    """
    polls = db.query(models.Poll).all()
    return polls

# --- Endpoint 3: Obtener una encuesta específica ---
@router.get("/polls/{poll_id}", response_model=schemas.Poll)
def get_poll(poll_id: int, db: Session = Depends(get_db)):
    """
    Retorna una encuesta específica por su ID.
    """
    poll = db.query(models.Poll).filter(models.Poll.id == poll_id).first()
    
    if poll is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Encuesta con id {poll_id} no encontrada")
    return poll

# --- Endpoint 4: Votar en una opción ---
@router.post("/vote/{option_id}", response_model=schemas.Option)
def vote_for_option(option_id: int, db: Session = Depends(get_db)):
    """
    Incrementa el contador de votos de una opción específica.
    """
    # Busca la opción en la base de datos
    db_option = db.query(models.Option).filter(models.Option.id == option_id).first()
    
    if db_option is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Opción con id {option_id} no encontrada")

    # Incrementa el contador y guarda
    db_option.vote_count += 1
    db.add(db_option)
    db.commit()
    
    # Refresca para obtener el nuevo 'vote_count'
    db.refresh(db_option)
    return db_option

# --- Endpoint 5: Health Check ---
# Este endpoint es CLAVE para la práctica.
# Nginx lo usará para saber si este backend está "vivo".
@router.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """
    Endpoint simple para que el balanceador de carga (Nginx)
    verifique si esta instancia del backend está viva.
    """
    return {"status": "ok"}