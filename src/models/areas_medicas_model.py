import uuid
from sqlalchemy import Column, CHAR, String, Enum, DateTime, Text, func
from sqlalchemy.orm import relationship
from src.db.db_mysql import databaseMysql
import enum

class EstatusEnum(str, enum.Enum):
    Activo = "Activo"
    Inactivo = "Inactivo"

class AreaMedica(databaseMysql.get_base()):
    __tablename__ = "tbc_areas_medicas"

    id = Column(CHAR(36), primary_key=True, server_default=func.uuid())
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    estatus = Column(Enum(EstatusEnum), nullable=True, default=EstatusEnum.Activo)
    fecha_registro = Column(DateTime, default=func.now(), nullable=False)
    fecha_actualizacion = Column(DateTime, onupdate=func.now())
    
    departamentos = relationship("Departamento", back_populates="area_medica")

    def __repr__(self):
        return f"<AreaMedica(id={self.id}, nombre={self.nombre}, estatus={self.estatus})>"