from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
import re
import uuid


class UsuarioBase(BaseModel):
    persona_id: Optional[str] = None
    nombre_usuario: str
    correo_electronico: EmailStr
    contrasena: str
    numero_telefonico_movil: str
    estatus: Optional[str] = "Activo"

    @field_validator("persona_id")
    @classmethod
    def validar_persona_id(cls, value):
        if value is None:
            raise ValueError("El campo 'persona_id' es obligatorio.")
        try:
            uuid.UUID(value)  # Verifica si es un UUID válido
        except ValueError:
            raise ValueError("El campo 'persona_id' debe ser un UUID válido.")
        return value

    @field_validator("nombre_usuario")
    @classmethod
    def validar_nombre_usuario(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("El campo 'nombre_usuario' no puede estar vacío.")
        if "  " in value:
            raise ValueError("El 'nombre_usuario' no puede contener espacios dobles.")
        if not re.match(r"^(?!.*\s{2})[\w.-]+$", value):
            raise ValueError("El 'nombre_usuario' solo puede contener letras, números, guiones bajos, puntos y ningún espacio doble.")
        return value

    @field_validator("contrasena")
    @classmethod
    def validar_contrasena(cls, value):
        if not re.match(r"^(?=.*\d)(?=.*).{8,30}$", value):
            raise ValueError("La contraseña debe contener al menos un dígito, una mayúscula y tener entre 8 y 30 caracteres.")
        return value
    
    @field_validator("numero_telefonico_movil")
    @classmethod
    def validar_numero_telefonico_movil(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("El campo 'numero_telefonico_movil' no puede estar vacío.")
        
        patron = re.compile(r"^\+\d{1,3} \d{3} \d{3} \d{4}$")
        if not patron.match(value):
            raise ValueError("El 'numero_telefonico_movil' debe seguir el formato: '+52 XXX XXX XXXX'.")
        return value

    @field_validator("estatus")
    @classmethod
    def validar_estatus(cls, value):
        if value not in ["Activo", "Inactivo", "Bloqueado", "Suspendido"]:
            raise ValueError("El 'estatus' solo puede ser 'Activo', 'Inactivo', 'Bloqueado' o 'Suspendido'.")
        return value


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioUpdate(BaseModel):
    nombre_usuario: Optional[str] = None
    correo_electronico: Optional[EmailStr] = None
    contrasena: Optional[str] = None
    numero_telefonico_movil: Optional[str] = None
    estatus: Optional[str] = None


class Usuario(UsuarioBase):
    id: str
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None

    model_config = {
        "from_attributes": True  # Equivalente a `orm_mode = True` en Pydantic v1
    }


class UsuarioLogin(BaseModel):
    nombre_usuario: str
    contrasena: str
    
    @field_validator("nombre_usuario")
    @classmethod
    def validar_nombre_usuario(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("El campo 'nombre_usuario' no puede estar vacío.")
        return value

    @field_validator("contrasena")
    @classmethod
    def validar_contrasena(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("El campo 'contrasena' no puede estar vacío.")
        return value
