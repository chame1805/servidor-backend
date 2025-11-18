# app/models.py

from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from .database import Base

print("--- ¡HOLA DESDE MODELS.PY! ---") # <-- Añadí esto para probar

class Poll(Base):
    __tablename__ = "polls"
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    options = relationship("Option", back_populates="poll")

class Option(Base):
    __tablename__ = "options"
    id = Column(Integer, primary_key=True, index=True)
    option_text = Column(String(255), nullable=False)
    vote_count = Column(Integer, default=0)
    poll_id = Column(Integer, ForeignKey("polls.id", ondelete="CASCADE"), nullable=False)
    poll = relationship("Poll", back_populates="options")