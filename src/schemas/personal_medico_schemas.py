from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import datetime
import uuid
import re


class PersonalMedicoBase(BaseModel):
    persona_id: str
    departamento_id: str
    cedula_profesional: str
    tipo: str
    especialidad: Optional[str] = None
    fecha_contratacion: datetime
    fecha_termino_contrato: Optional[datetime] = None
    salario: float
    estatus: Optional[str] = "Activo"

    @field_validator("persona_id", "departamento_id")
    @classmethod
    def validar_uuid(cls, value):
        try:
            uuid.UUID(value)
        except ValueError:
            raise ValueError("El valor debe ser un UUID válido.")
        return value

    @field_validator("cedula_profesional")
    @classmethod
    def validar_cedula(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("La cédula profesional no puede estar vacía.")
        if not re.match(r"^[a-zA-Z0-9]+$", value):
            raise ValueError("La cédula profesional solo puede contener letras y números.")
        return value

    @field_validator("tipo")
    @classmethod
    def validar_tipo(cls, value):
        tipos_validos = ["Médico", "Enfermero", "Administrativo", "Directivo", "Apoyo", "Residente", "Interno"]
        if value not in tipos_validos:
            raise ValueError(f"El 'tipo' debe ser uno de {tipos_validos}.")
        return value

    @field_validator("salario")
    @classmethod
    def validar_salario(cls, value):
        if value <= 0:
            raise ValueError("El salario debe ser mayor a 0.")
        return value

    @field_validator("estatus")
    @classmethod
    def validar_estatus(cls, value):
        if value not in ["Activo", "Inactivo"]:
            raise ValueError("El 'estatus' solo puede ser 'Activo' o 'Inactivo'.")
        return value


class PersonalMedicoCreate(PersonalMedicoBase):
    pass


class PersonalMedicoUpdate(BaseModel):
    departamento_id: Optional[str] = None
    especialidad: Optional[str] = None
    fecha_termino_contrato: Optional[datetime] = None
    salario: Optional[float] = None
    estatus: Optional[str] = None


class PersonalMedico(PersonalMedicoBase):
    id: str
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }
    
from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class PersonalMedicoResponse(BaseModel):
    personalId: str
    nombreCompleto: str
    genero: str
    fecha_nacimiento: date
    curp: str
    cedula_profesional: str
    especialidad: Optional[str] = None
    tipo: str
    fecha_contratacion: datetime
    fecha_termino_contrato: Optional[datetime] = None
    salario: float
    departamento: Optional[str] = None

    model_config = {
        "from_attributes":True
    }
