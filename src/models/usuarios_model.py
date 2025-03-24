import uuid
from sqlalchemy import Column, CHAR, String, Enum, DateTime, ForeignKey, func, text
from sqlalchemy.orm import relationship
from src.db.db_mysql import databaseMysql
import enum

class EstatusEnum(str, enum.Enum):
    Activo = "Activo"
    Inactivo = "Inactivo"
    Bloqueado = "Bloqueado"
    Suspendido = "Suspendido"

class Usuario(databaseMysql.get_base()):
    __tablename__ = "tbb_usuarios"

    id = Column(CHAR(36), primary_key=True, server_default=func.uuid())
    persona_id = Column(CHAR(36), ForeignKey("tbb_personas.id"), nullable=False)
    nombre_usuario = Column(String(40), unique=True, nullable=False)
    correo_electronico = Column(String(100), unique=True, nullable=False)
    contrasena = Column(String(40), nullable=False)
    numero_telefonico_movil = Column(CHAR(19), unique=True, nullable=False)
    estatus = Column(Enum(EstatusEnum), nullable=True, server_default=EstatusEnum.Activo)
    fecha_registro = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    fecha_actualizacion = Column(DateTime, server_onupdate=text("CURRENT_TIMESTAMP"))
    
    persona = relationship('Persona', back_populates='usuario')

    def __repr__(self):
        return f"<Usuario(id={self.id}, nombre_usuario={self.nombre_usuario}, correo_electronico={self.correo_electronico}, estatus={self.estatus})>"
