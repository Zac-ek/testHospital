from sqlalchemy.orm import Session
from src.models.citas_model import CitaMedica
from src.schemas.citas_schemas import CitaMedicaCreate, CitaMedicaUpdate

class CitasMedicasDAO:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CitasMedicasDAO, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        pass

    def create_cita(self, db: Session, cita: CitaMedicaCreate):
        db_cita = CitaMedica(**cita.model_dump())
        db.add(db_cita)
        db.commit()
        db.refresh(db_cita)
        return db_cita

    def get_cita_by_id(self, db: Session, cita_id: str):
        return db.query(CitaMedica).filter(CitaMedica.id == cita_id).first()

    def get_all_citas(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(CitaMedica).offset(skip).limit(limit).all()

    def update_cita(self, db: Session, cita_id: str, cita_update: CitaMedicaUpdate):
        db_cita = db.query(CitaMedica).filter(CitaMedica.id == cita_id).first()
        if not db_cita:
            return None
        for field, value in cita_update.model_dump(exclude_unset=True).items():
            setattr(db_cita, field, value)
        db.commit()
        db.refresh(db_cita)
        return db_cita

    def delete_cita(self, db: Session, cita_id: str):
        db_cita = db.query(CitaMedica).filter(CitaMedica.id == cita_id).first()
        if db_cita:
            db.delete(db_cita)
            db.commit()
            return True
        return False

citasDAO = CitasMedicasDAO()