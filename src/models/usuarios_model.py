import uuid
from sqlalchemy import Column, CHAR, String, Enum, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from src.db.db import db
import enum

class EstatusEnum(str, enum.Enum):
    Activo = "Activo"
    Inactivo = "Inactivo"
    Bloqueado = "Bloqueado"
    Suspendido = "Suspendido"

class Usuario(db.get_base()):
    __tablename__ = "tbb_usuarios"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    persona_id = Column(CHAR(36), unique=True, nullable=False)#, ForeignKey("tbb_personas.id", ondelete="CASCADE", onupdate="CASCADE")
    nombre_usuario = Column(String(40), unique=True, nullable=False)
    correo_electronico = Column(String(100), unique=True, nullable=False)
    contrasena = Column(String(40), nullable=False)
    estatus = Column(Enum(EstatusEnum), nullable=True, default=EstatusEnum.Activo)
    fecha_registro = Column(DateTime, default=func.now(), nullable=False)
    fecha_actualizacion = Column(DateTime, onupdate=func.now())

    # persona = relationship("Persona", back_populates="usuario")

    def __repr__(self):
        return f"<Usuario(id={self.id}, nombre_usuario={self.nombre_usuario}, correo_electronico={self.correo_electronico}, estatus={self.estatus})>"