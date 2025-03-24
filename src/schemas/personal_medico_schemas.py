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
        "from_attributes": True
    }