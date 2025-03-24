from sqlalchemy.orm import Session
from src.models.personas_model import Persona
from src.schemas.personas_schemas import PersonaCreate, PersonaUpdate

class PersonasDAO:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PersonasDAO, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Constructor de PersonasDAO"""
        pass

    def get_persona_by_id(self, db: Session, persona_id: str):
        return db.query(Persona).filter(Persona.id == persona_id).first()

    def get_persona_by_curp(self, db: Session, curp: str):
        return db.query(Persona).filter(Persona.curp == curp).first()

    def create_persona(self, db: Session, persona: PersonaCreate):
        db_persona = Persona(**persona.model_dump())
        db.add(db_persona)
        db.commit()
        db.refresh(db_persona)
        return db_persona

    def update_persona(self, db: Session, persona_id: str, persona_update: PersonaUpdate):
        db_persona = self.get_persona_by_id(db, persona_id)
        if not db_persona:
            return None
        for key, value in persona_update.model_dump(exclude_unset=True).items():
            setattr(db_persona, key, value)
        db.commit()
        db.refresh(db_persona)
        return db_persona

    def get_personas(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(Persona).offset(skip).limit(limit).all()

    def delete_persona(self, db: Session, persona_id: str):
        db_persona = self.get_persona_by_id(db, persona_id)
        if not db_persona:
            return None
        db.delete(db_persona)
        db.commit()
        return db_persona
    
personasDAO = PersonasDAO()
