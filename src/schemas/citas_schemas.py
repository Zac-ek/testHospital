from typing import Optional
from pydantic import BaseModel, field_validator, Field
from datetime import datetime, timezone
import re
import uuid


class CitaMedicaBase(BaseModel):
    personal_medico_id: str
    paciente_id: str
    servicio_medico_id: str
    folio: str
    tipo: str
    espacio_id: str
    fecha_programada: datetime | None = None
    observaciones: str


    @field_validator("personal_medico_id")
    @classmethod
    def validar_personal_medico_id(cls, value):
        if value is None:
            raise ValueError("El campo 'personal_medico_id' es obligatorio.")
        try:
            uuid.UUID(value)
        except ValueError:
            raise ValueError("El campo 'personal_medico_id' debe ser un UUID válido.")
        return value
    
    @field_validator("paciente_id")
    @classmethod
    def validar_Paciente_ID(cls, value):
        if value is None:
            raise ValueError("El campo 'Paciente_ID' es obligatorio.")
        try:
            uuid.UUID(value)
        except ValueError:
            raise ValueError("El campo 'Paciente_ID' debe ser un UUID válido.")
        return value
    
    @field_validator("servicio_medico_id")
    @classmethod
    def validar_Servicio_Medico_ID(cls, value):
        if value is None:
            raise ValueError("El campo 'Servicio_Medico_ID' es obligatorio.")
        try:
            uuid.UUID(value)
        except ValueError:
            raise ValueError("El campo 'Servicio_Medico_ID' debe ser un UUID válido.")
        return value
    
    @field_validator("folio")
    @classmethod
    def validar_folio(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("El campo 'nombre_usuario' no puede estar vacío.")
        if "  " in value:
            raise ValueError("El 'nombre_usuario' no puede contener espacios dobles.")
        if not re.match(r"^(?!.*\s{2})[\w.-]+$", value):
            raise ValueError("El 'nombre_usuario' solo puede contener letras, números, guiones bajos, puntos y ningún espacio doble.")
        return value
    
    @field_validator("tipo")
    @classmethod
    def validar_tipo(cls, value):
        if value not in ['Revisión', 'Diagnóstico', 'Tratamiento', 'Rehabilitación', 'Preoperatoria', 'Postoperatoria', 'Proceminientos', 'Seguimiento']:
            raise ValueError(" El valor solo puede ser 'Revisión', 'Diagnóstico', 'Tratamiento', 'Rehabilitación', 'Preoperatoria', 'Postoperatoria', 'Proceminientos', 'Seguimiento'")
        return value
    
    @field_validator("espacio_id")
    @classmethod
    def validar_Espacio_ID(cls, value):
        if value is None:
            raise ValueError("El campo 'Espacio_ID' es obligatorio.")
        try:
            uuid.UUID(value)
        except ValueError:
            raise ValueError("El campo 'Espacio_ID' debe ser un UUID válido.")
        return value
    
    @field_validator("fecha_programada")
    @classmethod
    def validar_fecha_programada(cls, value):
        if value is None:
            return value  # Permite valores nulos
        if not isinstance(value, datetime):
            raise ValueError("El campo 'Fecha_Programada' debe ser una fecha y hora válida.")
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
        # convertir a aware (UTC) si viene como naive
            value = value.replace(tzinfo=timezone.utc)
        if value < datetime.now(timezone.utc):
            raise ValueError("El campo 'Fecha_Programada' no puede ser una fecha pasada.")
        return value
    
    @field_validator("observaciones")
    @classmethod
    def validar_observaciones(cls, value):
        if value is None:
            raise ValueError("El campo 'observaciones' es obligatorio.")
        return value
        

class CitaMedicaCreate(CitaMedicaBase):
    pass


class CitaMedicaUpdate(BaseModel):
    estatus: Optional[str] = None


class CitaMedicaResponse(CitaMedicaBase):
    id: str
    fecha_inicio: Optional[datetime] = None
    fecha_termino: Optional[datetime] = None
    estatus: Optional[str] = None
    fecha_registro: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }
