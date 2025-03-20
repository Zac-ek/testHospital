from fastapi import HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.schemas.usuarios_schemas import UsuarioCreate, UsuarioLogin
from src.db.db import db
from src.dao.usuarios_dao import usuariosDAO
from src.helpers.jwt_config import jwt_config

class UsuariosController:
    """Clase controladora para manejar la lógica de usuario con patrón Singleton."""

    _instance = None  # Variable de clase para almacenar la única instancia

    def __new__(cls):
        """Implementa Singleton: Si no hay instancia, la crea."""
        if cls._instance is None:
            cls._instance = super(UsuariosController, cls).__new__(cls)
        return cls._instance

    def create_user(self, user: UsuarioCreate, db: Session = Depends(db.get_db)):
        """Crea un nuevo usuario en la base de datos."""
        db_user = usuariosDAO.get_user_by_username(db, username=user.nombre_usuario)
        if db_user:
            raise HTTPException(status_code=400, detail="Usuario existente, intenta nuevamente")
        return usuariosDAO.create_user(db=db, user=user)

    def read_credentials(self, usuario: UsuarioLogin, db: Session = Depends(db.get_db)):
        """Valida credenciales y genera un token de autenticación."""
        db_credentials = usuariosDAO.get_user_by_username(db, username=usuario.nombre_usuario)
        if db_credentials is None or db_credentials.contrasena != usuario.contrasena:
            return JSONResponse(content={'mensaje': 'Acceso denegado'}, status_code=404)

        token: str = jwt_config.solicita_token({"nombre_usuario": usuario.nombre_usuario})
        return JSONResponse(status_code=200, content={"token": token})
    
    async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(db.get_db)):
        db_users = usuariosDAO.get_users(db=db, skip=skip, limit=limit)
        return db_users

# Se obtiene la instancia única de UsuariosController
usuarios_controller = UsuariosController()
