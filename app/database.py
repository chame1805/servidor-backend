# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Cargar variables de entorno (del archivo .env)
load_dotenv()

# Lee la URL de la base de datos desde la variable de entorno
# Ejemplo en .env: DATABASE_URL="mysql+mysqlclient://usuario:contraseña@localhost/nombre_db"
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# --- Configuración de SQLAlchemy ---

# 1. El "motor" (engine) es el punto de entrada a la base de datos.
#    Aquí es donde se define la variable 'engine' que tu main.py está buscando
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 2. La "sesión" (SessionLocal) es la que realmente maneja la conversación
#    con la base de datos. Crearemos una de estas por cada petición.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. La "base" (Base) es una clase de la que heredarán todos nuestros
#    modelos (las tablas de la base de datos).
Base = declarative_base()

# --- Dependencia para inyectar la sesión en las rutas ---

# Esta función se usará en tus endpoints para obtener una sesión
# de base de datos y asegurarse de que se cierre correctamente.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()