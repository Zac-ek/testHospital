import uuid
import enum
from sqlalchemy import Column, CHAR, String, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from src.db.db_mysql import databaseMysql

class Departamento(databaseMysql.get_base()):
    __tablename__ = "tbc_departamentos"

    id = Column(CHAR(36), primary_key=True, server_default=func.uuid())
    nombre = Column(String(100), nullable=False)
    area_medica_id = Column(CHAR(36), ForeignKey("tbc_areas_medicas.id"), nullable=True)
    departamento_superior_id = Column(CHAR(36), ForeignKey("tbc_departamentos.id"), nullable=True)
    responsable_id = Column(CHAR(36), ForeignKey("tbb_personas.id"), nullable=True)  # Relación con Persona
    estatus = Column(Boolean, nullable=False, default=True)
    fecha_registro = Column(DateTime, default=func.now(), nullable=False)
    fecha_actualizacion = Column(DateTime, onupdate=func.now())

    area_medica = relationship("AreaMedica", back_populates="departamentos")
    personal_medico = relationship("PersonalMedico", back_populates="departamento")
    departamento_superior = relationship('Departamento', backref='subdepartamentos', remote_side=[id])
    responsable = relationship('Persona', back_populates='departamentos')

    def __repr__(self):
        return f"<Departamento(id={self.id}, nombre={self.nombre}, estatus={'Activo' if self.estatus else 'Inactivo'})>"

