from fastapi import APIRouter, Depends
from src.controllers.personal_medico_controller import personalMedicoController
from src.schemas.personal_medico_schemas import PersonalMedicoResponse
from src.middleware.auth_middleware import auth_middleware

class PersonalMedicoRoutes:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PersonalMedicoRoutes, cls).__new__(cls)
            cls._instance.router = APIRouter(prefix="/api/empleado", tags=["Personal Médico"])
            cls._instance.initialize_routes()
        return cls._instance

    def initialize_routes(self):
        self.router.get("/doctor/{id}", response_model=PersonalMedicoResponse, dependencies=[Depends(auth_middleware.autenticate_login)])(personalMedicoController.get_doctor)

personal_medico_routes = PersonalMedicoRoutes().router