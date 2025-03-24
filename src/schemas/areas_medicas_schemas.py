from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import datetime

class AreaMedicaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    estatus: Optional[str] = "Activo"

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("El campo 'nombre' no puede estar vacío.")
        return value

    @field_validator("estatus")
    @classmethod
    def validar_estatus(cls, value):
        if value not in ["Activo", "Inactivo"]:
            raise ValueError("El 'estatus' solo puede ser 'Activo' o 'Inactivo'.")
        return value

class AreaMedicaCreate(AreaMedicaBase):
    pass

class AreaMedicaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    estatus: Optional[str] = None

class AreaMedica(AreaMedicaBase):
    id: str
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }
