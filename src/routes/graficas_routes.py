from fastapi import APIRouter, Depends
from src.controllers.graficas_controller import graficas_controller
from src.controllers.grupos_sanguineos_controller import grupos_sanguineos_controller
from src.middleware.auth_middleware import auth_middleware

class GraficasRoutes:
    """Clase que maneja las rutas de las gráficas con un patrón Singleton."""

    _instance = None  # Variable de clase para almacenar la única instancia

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GraficasRoutes, cls).__new__(cls)
            cls._instance.router = APIRouter(prefix="/graficas", tags=["Gráficas"])
            cls._instance.initialize_routes()
        return cls._instance

    def initialize_routes(self):
        """Registra los endpoints en el router usando el controlador."""
        self.router.get("/hospital")(graficas_controller.obtener_estructura_hospital)
        self.router.get("/gruposSanguineos")(grupos_sanguineos_controller.obtener_todos)

# Se obtiene la única instancia de la clase y se usa en FastAPI
graficas_routes = GraficasRoutes().router
