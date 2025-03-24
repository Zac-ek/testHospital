from sqlalchemy.orm import Session
from src.models.areas_medicas_model import AreaMedica
from src.schemas.areas_medicas_schemas import AreaMedicaCreate, AreaMedicaUpdate

class AreasMedicasDAO:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AreasMedicasDAO, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Constructor de AreasMedicasDAO"""
        pass

    def get_area_medica_by_id(self, db: Session, area_id: str):
        """
        Obtiene un área médica por su ID.
        """
        return db.query(AreaMedica).filter(AreaMedica.id == area_id).first()

    def create_area_medica(self, db: Session, area: AreaMedicaCreate):
        """
        Crea una nueva área médica en la base de datos.
        """
        db_area = AreaMedica(
            nombre=area.nombre,
            descripcion=area.descripcion,
            estatus=area.estatus,
        )
        db.add(db_area)
        db.commit()
        db.refresh(db_area)
        return db_area

    def get_areas_medicas(self, db: Session, skip: int = 0, limit: int = 10):
        """
        Obtiene una lista de áreas médicas paginada.
        """
        return db.query(AreaMedica).offset(skip).limit(limit).all()

areasMedicasDAO = AreasMedicasDAO()
