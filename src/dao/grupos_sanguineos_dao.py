from sqlalchemy.orm import Session
from sqlalchemy import text

class GruposSanguineosDAO:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GruposSanguineosDAO, cls).__new__(cls)
        return cls._instance

    def obtener_todos(self, db: Session):
        query = text("SELECT * FROM vista_grupos_sanguineos")
        result = db.execute(query).mappings().all()
        return result

grupos_sanguineos_dao = GruposSanguineosDAO()
