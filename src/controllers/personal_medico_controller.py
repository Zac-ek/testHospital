from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from src.db.db_mysql import databaseMysql
from src.dao.personal_medico_dao import personalMedicoDAO

class PersonalMedicoController:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PersonalMedicoController, cls).__new__(cls)
        return cls._instance

    def get_doctor(self, doctor_id: str, db: Session = Depends(databaseMysql.get_db)):
        doctor = personalMedicoDAO.get_doctor_by_id(db, doctor_id)
        if not doctor:
            raise HTTPException(status_code=404, detail="No se encontró el doctor con ese ID")
        return doctor

personalMedicoController = PersonalMedicoController()