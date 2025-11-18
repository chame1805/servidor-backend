# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import polls

# --- Creación de Tablas ---
# Esto le dice a SQLAlchemy que cree las tablas de 'models.py'
# en tu base de datos MySQL si es que no existen.
models.Base.metadata.create_all(bind=engine)

# --- Instancia Principal de FastAPI ---
app = FastAPI(
    title="API de Encuestas",
    description="Backend para el proyecto de balanceo de carga",
    version="1.0.0"
)

# --- Configuración de CORS (Cross-Origin Resource Sharing) ---
# Esto es CRÍTICO para que un frontend (que vive en otro
# dominio/puerto) pueda hacer peticiones a este backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite cualquier origen (frontend)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todas las cabeceras
)

# --- Inclusión de Rutas ---
# Le dice a la app principal que incluya todos los endpoints
# definidos en el archivo app/routers/polls.py
app.include_router(polls.router)

# --- Ruta Raíz (Opcional) ---
# Un endpoint simple para verificar que la API está viva.
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Encuestas"}