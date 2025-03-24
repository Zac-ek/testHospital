from fastapi import HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.schemas.citas_schemas import CitaMedicaCreate, CitaMedicaUpdate
from src.db.db_mysql import databaseMysql
from src.dao.citas_dao import citasDAO

class CitasController:
    """Controlador para manejar operaciones sobre las citas médicas (Singleton)."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CitasController, cls).__new__(cls)
        return cls._instance

    def create_cita(self, cita: CitaMedicaCreate, db: Session = Depends(databaseMysql.get_db)):
        """Crea una nueva cita médica."""
        return citasDAO.create_cita(db=db, cita=cita)

    def read_cita(self, cita_id: str, db: Session = Depends(databaseMysql.get_db)):
        """Obtiene una cita médica por su ID."""
        db_cita = citasDAO.get_cita_by_id(db, cita_id)
        if db_cita is None:
            raise HTTPException(status_code=404, detail="Cita no encontrada")
        return db_cita

    def read_citas(self, skip: int = 0, limit: int = 10, db: Session = Depends(databaseMysql.get_db)):
        """Obtiene una lista paginada de citas médicas."""
        return citasDAO.get_all_citas(db=db, skip=skip, limit=limit)

    def update_cita(self, cita_id: str, cita_update: CitaMedicaUpdate, db: Session = Depends(databaseMysql.get_db)):
        """Actualiza una cita médica existente."""
        updated_cita = citasDAO.update_cita(db, cita_id=cita_id, cita_update=cita_update)
        if updated_cita is None:
            raise HTTPException(status_code=404, detail="Cita no encontrada")
        return updated_cita

    def delete_cita(self, cita_id: str, db: Session = Depends(databaseMysql.get_db)):
        """Elimina una cita médica por su ID."""
        success = citasDAO.delete_cita(db, cita_id)
        if not success:
            raise HTTPException(status_code=404, detail="Cita no encontrada")
        return JSONResponse(status_code=200, content={"mensaje": "Cita eliminada correctamente"})

# Instancia única del controlador
citas_controller = CitasController()
