from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from datetime import datetime
from bson import ObjectId
import uuid

# Pydantic no reconoce directamente ObjectId, así que creamos un validador personalizado
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler: GetJsonSchemaHandler) -> JsonSchemaValue:
        return {
            "type": "string",
            "example": "507f1f77bcf86cd799439011",
            "title": "ObjectId",
        }

class NotaMedicaBase(BaseModel):
    pacienteId: str = Field(...)
    personal_medicoId: str = Field(...)
    fechaNota: datetime = Field(...)
    sintomas: List[str] = Field(...)
    diagnostico: str = Field(...)
    tratamiento: str = Field(...)
    observaciones: str = Field(...)
    fechaSeguimiento: datetime = Field(...)

    @field_validator("pacienteId", "personal_medicoId")
    @classmethod
    def validar_uuid(cls, value):
        try:
            uuid.UUID(value)
        except ValueError:
            raise ValueError("El valor debe ser un UUID válido")
        return value

class NotaMedicaCreate(NotaMedicaBase):
    pass

class NotaMedicaUpdate(BaseModel):
    fechaNota: Optional[datetime] = None
    sintomas: Optional[List[str]] = None
    diagnostico: Optional[str] = None
    tratamiento: Optional[str] = None
    observaciones: Optional[str] = None
    fechaSeguimiento: Optional[datetime] = None

class NotaMedicaResponse(NotaMedicaBase):
    id: PyObjectId = Field(alias="_id")
    createdAt: datetime
    updatedAt: datetime

    model_config = {
        "populate_by_name": True,
        "from_attributes": True,
        "json_encoders": {
            ObjectId: str
        }
    }
