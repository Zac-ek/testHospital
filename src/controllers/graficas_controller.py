from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from src.db.db_mysql import databaseMysql
from src.models.index_models import *
from src.models.personas_model import Persona


class GraficasController:
    """Clase controladora para manejar la lógica de las gráficas con patrón Singleton."""

    _instance = None  # Variable de clase para almacenar la única instancia

    def __new__(cls):
        """Implementa Singleton: Si no hay instancia, la crea."""
        if cls._instance is None:
            cls._instance = super(GraficasController, cls).__new__(cls)
        return cls._instance

    def obtener_estructura_hospital(self, db: Session = Depends(databaseMysql.get_db)):
        """Obtiene los datos necesarios para generar la estructura JSON de la gráfica."""

        # Obtener todas las áreas médicas
        areas_medicas = db.query(AreaMedica).all()

        # Construir la estructura JSON
        json_data = {
            "name": "Hospital",
            "responsable": "Director General",
            "children": []
        }

        for area in areas_medicas:
            area_data = {
                "name": area.nombre,
                "children": []
            }

            # Obtener departamentos de cada área médica
            departamentos = db.query(Departamento).filter(Departamento.area_medica_id == area.id).all()

            for departamento in departamentos:
                responsable = db.query(Persona).filter(Persona.id == departamento.responsable_id).first()
                responsable_nombre = f"{responsable.nombre} {responsable.primer_apellido} {responsable.segundo_apellido}" if responsable else "Sin Responsable"

                departamento_data = {
                    "id": departamento.id,
                    "name": departamento.nombre,
                    "responsable": responsable_nombre,
                    "children": []
                }

                # Obtener el personal médico del departamento
                personal_medico = db.query(PersonalMedico).filter(PersonalMedico.departamento_id == departamento.id).all()

                if personal_medico:
                    personal_data = {
                        "name": "Personal Medico",
                        "children": []
                    }

                    for personal in personal_medico:
                        persona = db.query(Persona).filter(Persona.id == personal.persona_id).first()
                        if persona:
                            personal_data["children"].append({
                                "personalId": personal.id,
                                "name": f"{persona.nombre} {persona.primer_apellido} {persona.segundo_apellido}",
                                "tipo": "doctor" if personal.tipo == "Médico" else "enfermero"
                            })

                    departamento_data["children"].append(personal_data)

                area_data["children"].append(departamento_data)

            json_data["children"].append(area_data)

        return JSONResponse(content=json_data, status_code=200)


# Se obtiene la instancia única del controlador
graficas_controller = GraficasController()
