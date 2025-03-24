from fastapi import FastAPI, WebSocket, WebSocketDisconnect,  HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from src.db.db_mysql import databaseMysql
from src.routes.usuarios_routes import usuario_routes
from src.routes.notas_medicas_routes import notasMedicasRoutes
from src.routes.graficas_routes import graficas_routes
from src.routes.citas_routes import citas_routes
from src.routes.personal_medico_routes import personal_medico_routes
from fastapi.responses import JSONResponse
from typing import List
import jwt
import os
from uuid import uuid4
from src.helpers.jwt_config import jwt_config

class HospitalBackend:
    """Clase Singleton para manejar la configuración y creación de la aplicación FastAPI."""

    _instance = None  # Variable de clase para almacenar la única instancia

    def __new__(cls):
        """Implementa el patrón Singleton asegurando una única instancia."""
        if cls._instance is None:
            cls._instance = super(HospitalBackend, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Inicializa la configuración de la aplicación FastAPI."""
        # Inicialización de la aplicación FastAPI
        self.app = FastAPI(
            redirect_slashes=False,
            title="Backend del hospital",
            description="Backend del hospital",
        )

        # Lista de clientes conectados para manejar múltiples conexiones WebSocket
        self.clients: dict[str, WebSocket] = {}  # Cambiado a un diccionario
        
        # Configuración de CORS
        self._configure_cors()

        # Inclusión de rutas
        self._include_routes()

        # Incluir el WebSocket
        self._include_websocket()

        # Base de datos y creación de tablas
        self._configure_database()

    def _configure_cors(self):
        """Configura las opciones CORS para permitir peticiones desde Angular"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Permitir solicitudes desde Angular
            allow_credentials=True,
            allow_methods=["*"],  # Permitir todos los métodos HTTP
            allow_headers=["*"],  # Permitir todos los encabezados
        )

    def _configure_database(self):
        """Configura la base de datos y crea las tablas"""
        Base = databaseMysql.get_base()
        Base.metadata.create_all(bind=databaseMysql.get_engine())

    def _include_routes(self):
        """Incluye las rutas en la aplicación FastAPI"""
        self.app.include_router(usuario_routes)
        self.app.include_router(notasMedicasRoutes)
        self.app.include_router(graficas_routes)
        self.app.include_router(citas_routes)
        self.app.include_router(personal_medico_routes)

    def _include_websocket(self):
        """Incluye el WebSocket en la aplicación FastAPI."""
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """Maneja la conexión WebSocket con autenticación y manejo de clientes."""
            
            # Verificar si el token existe en los encabezados
            print(websocket.query_params)
            token = websocket.query_params.get("token")  # Cambié de request.headers a websocket.headers
            print(token)
            if not token:
                print("Estoy en el if D,:")
                await websocket.close()
                return

            # Verificar el token JWT (simulando la validación similar al middleware de auth)
            try:
                # Decodificar y validar el token (este paso puede involucrar tu lógica de autenticación personalizada)
                payload = jwt_config.valida_token(token)

                # Obtener clientId, si no existe generar uno
                client_id = str(uuid4())

                # Manejo de desconexión previa
                if client_id in self.clients:
                    self.clients[client_id].close()

                # Asignar la conexión WebSocket al cliente
                self.clients[client_id] = websocket
                await websocket.accept()
                await websocket.send_text(f"Conexión establecida con el clientId: {client_id}")

                try:
                    # Escuchar mensajes del cliente
                    while True:
                        message = await websocket.receive_text()
                        # Aquí puedes agregar la lógica de cómo procesar los mensajes de cada cliente
                        await websocket.send_text(f"Mensaje recibido: {message}")
                except WebSocketDisconnect:
                    # Manejo de desconexión
                    del self.clients[client_id]
                    print(f"Cliente {client_id} desconectado")
            except jwt.ExpiredSignatureError:
                await websocket.close(code=1008)  # Cerrar si el token expiró
            except jwt.InvalidTokenError:
                await websocket.close(code=1008)  # Cerrar si el token no es válido


    def get_app(self):
        """Devuelve la instancia de la aplicación FastAPI"""
        return self.app


# Crear la instancia única
app_instance = HospitalBackend()
app = app_instance.get_app()

# MANEJADORES DE EXCEPCIONES GLOBALES
# ----------------------------------
# Aseguran que, ante cualquier error (incluso 401, 403, 500, etc.), 
# la respuesta incluya encabezados CORS. 

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Error interno en el servidor: {exc}"},
        headers={"Access-Control-Allow-Origin": "*"}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers={"Access-Control-Allow-Origin": "*"}
    )