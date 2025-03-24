from sqlalchemy.orm import Session
from src.models.departamentos_model import Departamento
from src.schemas.departamentos_schemas import DepartamentoCreate, DepartamentoUpdate

class DepartamentosDAO:
    _instance = None

    def __new__(cls):
        """Implementa el patrón Singleton para asegurar una única instancia."""
        if cls._instance is None:
            cls._instance = super(DepartamentosDAO, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Constructor de DepartamentosDAO"""
        pass

    def get_departamento_by_id(self, db: Session, departamento_id: str):
        """
        Obtiene un departamento por su ID.
        """
        return db.query(Departamento).filter(Departamento.id == departamento_id).first()

    def create_departamento(self, db: Session, departamento: DepartamentoCreate):
        """
        Crea un nuevo departamento en la base de datos.
        """
        db_departamento = Departamento(
            nombre=departamento.nombre,
            area_medica_id=departamento.area_medica_id,
            departamento_superior_id=departamento.departamento_superior_id,
            responsable_id=departamento.responsable_id,
            estatus=departamento.estatus,
        )
        db.add(db_departamento)
        db.commit()
        db.refresh(db_departamento)
        return db_departamento

    def get_departamentos(self, db: Session, skip: int = 0, limit: int = 10):
        """
        Obtiene una lista de departamentos paginada.
        """
        return db.query(Departamento).offset(skip).limit(limit).all()

departamentosDAO = DepartamentosDAO()
