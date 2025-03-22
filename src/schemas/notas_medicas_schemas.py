from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime, timezone
from typing import List

class PyObjectId(ObjectId):
    """Clase personalizada para manejar ObjectId en Pydantic."""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise ValueError("Invalid ObjectId")
        return str(v)

class NotaMedicaModel(BaseModel):
    id: PyObjectId = Field(default_factory=ObjectId, alias="_id")
    pacienteId: str
    personal_medicoId: str
    fechaNota: datetime
    sintomas: List[str]
    diagnostico: str
    tratamiento: int
    observaciones: str
    fechaSeguimiento: datetime
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}  # Convierte ObjectId a string en JSON
