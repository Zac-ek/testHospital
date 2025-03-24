from fastapi import Depends
from src.db.db_mysql import databaseMysql
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.models.personas_model import Persona
from sqlalchemy import text

class GruposSanguineosDAO:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GruposSanguineosDAO, cls).__new__(cls)
        return cls._instance

    def obtener_todos(self, db: Session):
        total_personas = db.query(func.count(Persona.id)).scalar()

        if total_personas == 0:
            return []

        resultados = (
            db.query(
                Persona.grupo_sanguineo.label("Grupo_Sanguineo"),
                func.count(Persona.id).label("cantidad_personas"),
                func.round((func.count(Persona.id) * 100.0) / total_personas, 2).label("porcentaje")
            )
            .group_by(Persona.grupo_sanguineo)
            .order_by(func.count(Persona.id).desc())
            .all()
        )

        # Convertir los resultados a una lista de diccionarios
        return [
            {
                "Grupo_Sanguineo": resultado.Grupo_Sanguineo,
                "cantidad_personas": resultado.cantidad_personas,
                "porcentaje": resultado.porcentaje
            }
            for resultado in resultados
        ]

grupos_sanguineos_dao = GruposSanguineosDAO()
