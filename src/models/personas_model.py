import uuid
from sqlalchemy import Column, CHAR, String, Enum, Date, DateTime, func, Boolean
from sqlalchemy.orm import relationship
from src.db.db_mysql import databaseMysql
import enum

class GeneroEnum(str, enum.Enum):
    M = "M"
    F = "F"
    NB = "N/B"

class GrupoSanguineoEnum(str, enum.Enum):
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    AB_POS = "AB+"
    AB_NEG = "AB-"
    O_POS = "O+"
    O_NEG = "O-"


class Persona(databaseMysql.get_base()):
    __tablename__ = "tbb_personas"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    titulo = Column(String(20), nullable=True)
    nombre = Column(String(80), nullable=False)
    primer_apellido = Column(String(80), nullable=False)
    segundo_apellido = Column(String(80), nullable=True)
    curp = Column(String(18), unique=True, nullable=True)
    genero = Column(Enum(GeneroEnum), nullable=False)
    grupo_sanguineo = Column(Enum("A+","A-","B+","B-","AB+","AB-","O+","O-"), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    estatus = Column(Boolean, nullable=False, default=True)
    fecha_registro = Column(DateTime, default=func.now(), nullable=False)
    fecha_actualizacion = Column(DateTime, onupdate=func.now())
    
    departamentos = relationship('Departamento', back_populates='responsable')
    personal_medico = relationship('PersonalMedico', back_populates='persona')
    usuario = relationship('Usuario', back_populates='persona')

    def __repr__(self):
        return f"<Persona(id={self.id}, nombre={self.nombre}, primer_apellido={self.primer_apellido})>"
