from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime, date
import re
import uuid


class PersonaBase(BaseModel):
    titulo: Optional[str] = None
    nombre: str
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    curp: Optional[str] = None
    genero: str
    grupo_sanguineo: str
    fecha_nacimiento: date
    estatus: Optional[bool] = True

    @field_validator("titulo")
    @classmethod
    def validar_titulo(cls, value):
        if value:
            value = value.strip()
            if not re.match(r"^[A-Za-z. ]{1,20}$", value):
                raise ValueError("El 'título' solo puede contener letras, puntos y espacios, con un máximo de 20 caracteres.")
        return value

    @field_validator("nombre", "primer_apellido", "segundo_apellido", mode="before")
    @classmethod
    def validar_nombre_y_apellidos(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Este campo no puede estar vacío.")
        if not re.match(r"^[A-Za-z ]{1,80}$", value):
            raise ValueError("Este campo solo puede contener letras y espacios, con un máximo de 80 caracteres.")
        return value

    @field_validator("curp")
    @classmethod
    def validar_curp(cls, value):
        if value:
            value = value.strip().upper()
            patron_curp = re.compile(r"^[A-Z]{4}\d{6}[HM][A-Z]{5}[0-9A-Z]\d$")
            if not patron_curp.match(value):
                raise ValueError("El 'CURP' no es válido.")
        return value

    @field_validator("genero")
    @classmethod
    def validar_genero(cls, value):
        if value not in ["M", "F", "N/B"]:
            raise ValueError("El 'género' solo puede ser 'M', 'F' o 'N/B'.")
        return value

    @field_validator("grupo_sanguineo")
    @classmethod
    def validar_grupo_sanguineo(cls, value):
        if value not in ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]:
            raise ValueError("El 'grupo sanguíneo' no es válido.")
        return value

    @field_validator("fecha_nacimiento")
    @classmethod
    def validar_fecha_nacimiento(cls, value):
        if value > datetime.now().date():
            raise ValueError("La 'fecha de nacimiento' no puede ser en el futuro.")
        return value


class PersonaCreate(PersonaBase):
    pass


class PersonaUpdate(BaseModel):
    titulo: Optional[str] = None
    nombre: Optional[str] = None
    primer_apellido: Optional[str] = None
    segundo_apellido: Optional[str] = None
    curp: Optional[str] = None
    genero: Optional[str] = None
    grupo_sanguineo: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    estatus: Optional[bool] = None


class Persona(PersonaBase):
    id: str
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None

    model_config = {
        "from_attributes": True  # Equivalente a `orm_mode = True` en Pydantic v1
    }
