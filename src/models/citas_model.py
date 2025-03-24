import uuid
from sqlalchemy import Column, CHAR, String, Enum, DateTime, Text, func
from src.db.db_mysql import databaseMysql
import enum

class TipoCitaEnum(str, enum.Enum):
    Revisión = "Revisión"
    Diagnóstico = "Diagnóstico"
    Tratamiento = "Tratamiento"
    Rehabilitación = "Rehabilitación"
    Preoperatoria = "Preoperatoria"
    Postoperatoria = "Postoperatoria"
    Proceminientos = "Proceminientos"
    Seguimiento = "Seguimiento"

class EstatusCitaEnum(str, enum.Enum):
    Programada = "Programada"
    Atendida = "Atendida"
    Cancelada = "Cancelada"
    Reprogramada = "Reprogramada"
    NoAtendida = "No atendida"
    EnProceso = "En proceso"

class CitaMedica(databaseMysql.get_base()):
    __tablename__ = "tbb_citas_medicas"

    id = Column("ID", CHAR(36), primary_key=True, server_default=func.uuid())
    personal_medico_id = Column("Personal_Medico_ID", CHAR(36), nullable=False)
    paciente_id = Column("Paciente_ID", CHAR(36), nullable=False)
    servicio_medico_id = Column("Servicio_Medico_ID", CHAR(36), nullable=False)
    folio = Column("Folio", String(60), unique=True, nullable=False)
    tipo = Column("Tipo", Enum(TipoCitaEnum), nullable=False)
    espacio_id = Column("Espacio_ID", CHAR(36), nullable=False)
    fecha_programada = Column("Fecha_Programada", DateTime, default=func.now(), nullable=False)
    fecha_inicio = Column("Fecha_Inicio", DateTime, nullable=True)
    fecha_termino = Column("Fecha_Termino", DateTime, nullable=True)
    observaciones = Column("Observaciones", Text, nullable=False)
    estatus = Column("Estatus", Enum(EstatusCitaEnum), default=EstatusCitaEnum.Programada, nullable=False)
    fecha_registro = Column("Fecha_Registro", DateTime, default=func.now(), nullable=False)
    fecha_actualizacion = Column("Fecha_Actualizacion", DateTime, nullable=True, onupdate=func.now())

    def __repr__(self):
        return f"<CitaMedica(id={self.id}, folio={self.folio}, tipo={self.tipo}, estatus={self.estatus})>"
