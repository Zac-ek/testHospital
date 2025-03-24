from sqlalchemy.orm import Session
from src.models.personal_medico_model import PersonalMedico
from src.schemas.personal_medico_schemas import PersonalMedicoCreate, PersonalMedicoUpdate


class PersonalMedicoDAO:
    _instance = None

    def __new__(cls):
        """Implementa el patrón Singleton para asegurar una única instancia."""
        if cls._instance is None:
            cls._instance = super(PersonalMedicoDAO, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Constructor de PersonalMedicoDAO"""
        pass

    def get_by_cedula(self, db: Session, cedula_profesional: str):
        """Obtiene un registro por cédula profesional."""
        return db.query(PersonalMedico).filter(PersonalMedico.cedula_profesional == cedula_profesional).first()

    def create(self, db: Session, personal: PersonalMedicoCreate):
        """Crea un nuevo registro de personal médico."""
        db_personal = PersonalMedico(
            persona_id=personal.persona_id,
            departamento_id=personal.departamento_id,
            cedula_profesional=personal.cedula_profesional,
            tipo=personal.tipo,
            especialidad=personal.especialidad,
            fecha_contratacion=personal.fecha_contratacion,
            fecha_termino_contrato=personal.fecha_termino_contrato,
            salario=personal.salario,
            estatus=personal.estatus,
        )
        db.add(db_personal)
        db.commit()
        db.refresh(db_personal)
        return db_personal

    def get_all(self, db: Session, skip: int = 0, limit: int = 10):
        """Obtiene una lista paginada del personal médico."""
        return db.query(PersonalMedico).offset(skip).limit(limit).all()

    def update(self, db: Session, personal_id: str, update_data: PersonalMedicoUpdate):
        """Actualiza un registro de personal médico."""
        db_personal = db.query(PersonalMedico).filter(PersonalMedico.id == personal_id).first()
        if db_personal:
            for key, value in update_data.dict(exclude_unset=True).items():
                setattr(db_personal, key, value)
            db.commit()
            db.refresh(db_personal)
        return db_personal

    def delete(self, db: Session, personal_id: str):
        """Elimina un registro de personal médico."""
        db_personal = db.query(PersonalMedico).filter(PersonalMedico.id == personal_id).first()
        if db_personal:
            db.delete(db_personal)
            db.commit()
        return db_personal


personalMedicoDAO = PersonalMedicoDAO()
