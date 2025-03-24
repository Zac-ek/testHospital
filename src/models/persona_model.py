from sqlalchemy import Column, String, Date, Enum, DateTime, CHAR
from src.db.db_mysql import databaseMysql

class Persona(databaseMysql.get_base()):
    __tablename__ = "tbb_personas"

    id = Column("ID", CHAR(36), primary_key=True)
    titulo = Column("Titulo", String(20))
    nombre = Column("Nombre", String(80))
    primer_apellido = Column("Primer_Apellido", String(80))
    segundo_apellido = Column("Segundo_Apellido", String(80))
    curp = Column("CURP", String(18))
    genero = Column("Genero", Enum("M", "F", "N/B"))
    grupo_sanguineo = Column("Grupo_Sanguineo", Enum("A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"))
    fecha_nacimiento = Column("Fecha_Nacimiento", Date)
    estatus = Column("Estatus", String(1))
    fecha_registro = Column("Fecha_Registro", DateTime)
    fecha_actualizacion = Column("Fecha_Actualizacion", DateTime)