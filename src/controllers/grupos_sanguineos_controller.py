from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.db_mysql import databaseMysql
from src.dao.grupos_sanguineos_dao import grupos_sanguineos_dao

class GruposSanguineosController:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GruposSanguineosController, cls).__new__(cls)
        return cls._instance

    def obtener_todos(self, db: Session = Depends(databaseMysql.get_db)):
        try:
            return grupos_sanguineos_dao.obtener_todos(db)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error al obtener grupos sanguíneos")

grupos_sanguineos_controller = GruposSanguineosController()
