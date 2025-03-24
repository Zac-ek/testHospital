from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import datetime
import uuid

class DepartamentoBase(BaseModel):
    nombre: str
    area_medica_id: Optional[str] = None
    departamento_superior_id: Optional[str] = None
    responsable_id: Optional[str] = None
    estatus: Optional[bool] = True

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("El campo 'nombre' no puede estar vacío.")
        return value

    @field_validator("area_medica_id", "departamento_superior_id", "responsable_id", mode="before")
    @classmethod
    def validar_uuid(cls, value):
        if value is not None:
            try:
                uuid.UUID(value)  # Verifica si es un UUID válido
            except ValueError:
                raise ValueError("El campo debe ser un UUID válido.")
        return value

class DepartamentoCreate(DepartamentoBase):
    pass

class DepartamentoUpdate(BaseModel):
    nombre: Optional[str] = None
    area_medica_id: Optional[str] = None
    departamento_superior_id: Optional[str] = None
    responsable_id: Optional[str] = None
    estatus: Optional[bool] = None

class Departamento(DepartamentoBase):
    id: str
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }
