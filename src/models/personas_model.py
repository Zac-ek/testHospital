import uuid
from sqlalchemy import Column, CHAR, String, Enum, Date, DateTime, func, Boolean, text
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

    id = Column(CHAR(36), primary_key=True, server_default=func.uuid())
    titulo = Column(String(20), nullable=True)
    nombre = Column(String(80), nullable=False)
    primer_apellido = Column(String(80), nullable=False)
    segundo_apellido = Column(String(80), nullable=True)
    curp = Column(String(18), unique=True, nullable=True)
    genero = Column("Genero", Enum("M", "F", "N/B"), nullable=False)
    grupo_sanguineo = Column(Enum("A+","A-","B+","B-","AB+","AB-","O+","O-"), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    estatus = Column(Boolean, nullable=False, server_default=text("1"))
    fecha_registro = Column("Fecha_Registro", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")) 
    fecha_actualizacion = Column("Fecha_Actualizacion", DateTime, nullable=True,server_onupdate=text("CURRENT_TIMESTAMP"))
    
    departamentos = relationship('Departamento', back_populates='responsable')
    personal_medico = relationship('PersonalMedico', back_populates='persona')
    usuario = relationship('Usuario', back_populates='persona')

    def __repr__(self):
        return f"<Persona(id={self.id}, nombre={self.nombre}, primer_apellido={self.primer_apellido})>"
