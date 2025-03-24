from sqlalchemy import Column, String, DateTime, Float, CHAR, Enum, ForeignKey
from src.db.db_mysql import databaseMysql

class PersonalMedico(databaseMysql.get_base()):
    __tablename__ = "tbb_personal_medico"

    persona_id = Column("Persona_ID", CHAR(36), primary_key=True)
    departamento_id = Column("Departamento_ID", CHAR(36), ForeignKey("tbc_departamentos.ID"))
    cedula_profesional = Column("Cedula_Profesional", String(100))
    especialidad = Column("Especialidad", String(255))
    tipo = Column("Tipo", Enum('Médico', 'Enfermero', 'Administrativo', 'Directivo', 'Apoyo', 'Residente', 'Interno'))
    fecha_contratacion = Column("Fecha_Contratacion", DateTime)
    fecha_termino_contrato = Column("Fecha_Termino_Contrato", DateTime)
    salario = Column("Salario", Float)
    estatus = Column("Estatus", Enum('Activo', 'Inactivo'))
    fecha_registro = Column("Fecha_Registro", DateTime)
    fecha_actualizacion = Column("Fecha_Actualizacion", DateTime)