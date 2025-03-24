from fastapi import APIRouter, Depends
from src.controllers.usuarios_controller import usuarios_controller
from src.schemas.usuarios_schemas import Usuario
from src.middleware.auth_middleware import auth_middleware

class UsuarioRoutes:
    """Clase que maneja las rutas de usuario con un patrón Singleton."""

    _instance = None  # Variable de clase para almacenar la única instancia

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UsuarioRoutes, cls).__new__(cls)
            cls._instance.router = APIRouter(prefix="/users", tags=["Usuarios"])
            cls._instance.initialize_routes()
        return cls._instance

    def initialize_routes(self):
        """Registra los endpoints en el router usando el controlador."""
        self.router.post("/register", response_model=Usuario)(usuarios_controller.create_user)
        self.router.post("/login")(usuarios_controller.read_credentials)
        self.router.get("/getAll", response_model=list[Usuario], dependencies=[Depends(auth_middleware.autenticate_login)])(usuarios_controller.read_users)

# Se obtiene la única instancia de la clase y se usa en FastAPI
usuario_routes = UsuarioRoutes().router
