import uuid
from sqlalchemy import Column, CHAR, String, Enum, DateTime, ForeignKey, DECIMAL, func, text
from sqlalchemy.orm import relationship
from src.db.db_mysql import databaseMysql
import enum


class TipoPersonalEnum(str, enum.Enum):
    Medico = "Médico"
    Enfermero = "Enfermero"
    Administrativo = "Administrativo"
    Directivo = "Directivo"
    Apoyo = "Apoyo"
    Residente = "Residente"
    Interno = "Interno"


class EstatusPersonalEnum(str, enum.Enum):
    Activo = "Activo"
    Inactivo = "Inactivo"


class PersonalMedico(databaseMysql.get_base()):
    __tablename__ = "tbb_personal_medico"

    id = Column(CHAR(36), primary_key=True, server_default=func.uuid())
    persona_id = Column(CHAR(36), ForeignKey("tbb_personas.id"), nullable=False)
    departamento_id = Column(CHAR(36), ForeignKey("tbc_departamentos.id"), nullable=False)
    cedula_profesional = Column(String(100), unique=True, nullable=False)
    tipo = Column(Enum(TipoPersonalEnum), nullable=False)
    especialidad = Column(String(255), nullable=True)
    fecha_registro = Column("Fecha_Registro", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    fecha_contratacion = Column(DateTime, nullable=False)
    fecha_termino_contrato = Column(DateTime, nullable=True)
    salario = Column(DECIMAL(10, 2), nullable=False)
    estatus = Column(Enum(EstatusPersonalEnum), server_default=EstatusPersonalEnum.Activo, nullable=False)
    fecha_actualizacion = Column("Fecha_Actualizacion", DateTime, nullable=True,server_onupdate=text("CURRENT_TIMESTAMP"))
    
    departamento = relationship("Departamento", back_populates="personal_medico")
    persona = relationship('Persona', back_populates='personal_medico')

    def __repr__(self):
        return f"<PersonalMedico(id={self.id}, cedula_profesional={self.cedula_profesional}, tipo={self.tipo}, estatus={self.estatus})>"
