from sqlalchemy.orm import Session
from src.models.personal_medico_model import PersonalMedico
from src.schemas.personal_medico_schemas import PersonalMedicoCreate, PersonalMedicoUpdate
from sqlalchemy import text

class PersonalMedicoDAO:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PersonalMedicoDAO, cls).__new__(cls)
        return cls._instance

    def get_doctor_by_id(self, db: Session, doctor_id: str):
        query = text("""
            SELECT 
                pm.Persona_ID AS personalId,
                CONCAT_WS(' ', p.Nombre, p.Primer_Apellido, p.Segundo_Apellido) AS nombreCompleto,
                p.genero,
                p.fecha_nacimiento,
                p.CURP AS curp,
                pm.Cedula_Profesional AS cedula_profesional,
                pm.Especialidad AS especialidad,
                pm.Tipo AS tipo,
                pm.Fecha_Contratacion AS fecha_contratacion,
                pm.Fecha_Termino_Contrato AS fecha_termino_contrato,
                pm.Salario AS salario,
                d.Nombre AS departamento
            FROM tbb_personal_medico pm
            LEFT JOIN tbb_personas p ON pm.Persona_ID = p.ID
            LEFT JOIN tbc_departamentos d ON pm.Departamento_ID = d.ID
            WHERE pm.Persona_ID = :doctor_id
            LIMIT 1
        """)
        result = db.execute(query, {"doctor_id": doctor_id}).mappings().fetchone()
        return result

personalMedicoDAO = PersonalMedicoDAO()
