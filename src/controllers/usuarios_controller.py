from fastapi import HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.schemas.usuarios_schemas import UsuarioCreate, UsuarioLogin
from src.db.db_mysql import databaseMysql
from src.models.index_models import *
from src.dao.usuarios_dao import usuariosDAO
from src.helpers.jwt_config import jwt_config
from datetime import date
from decimal import Decimal

class UsuariosController:
    """Clase controladora para manejar la lógica de usuario con patrón Singleton."""

    _instance = None  # Variable de clase para almacenar la única instancia

    def __new__(cls):
        """Implementa Singleton: Si no hay instancia, la crea."""
        if cls._instance is None:
            cls._instance = super(UsuariosController, cls).__new__(cls)
        return cls._instance

    def create_user(self, user: UsuarioCreate, db: Session = Depends(databaseMysql.get_db)):
        """Crea un nuevo usuario en la base de datos."""
        db_user = usuariosDAO.get_user_by_username(db, username=user.nombre_usuario)
        if db_user:
            raise HTTPException(status_code=400, detail="Usuario existente, intenta nuevamente")
        return usuariosDAO.create_user(db=db, user=user)

    from datetime import date

    def read_credentials(self, usuario: UsuarioLogin, db: Session = Depends(databaseMysql.get_db)):
        """Valida credenciales y genera un token de autenticación con información extendida."""
        db_credentials = db.query(Usuario).filter(
            Usuario.nombre_usuario == usuario.nombre_usuario,
            Usuario.contrasena == usuario.contrasena
        ).first()

        if db_credentials is None:
            return JSONResponse(content={'mensaje': 'Acceso denegado'}, status_code=404)

        # Obtener la información de la persona y el personal médico asociado
        persona = db_credentials.persona
        personal_medico = db.query(PersonalMedico).filter(
            PersonalMedico.persona_id == persona.id
        ).first() if persona else None

        tipo_personal = personal_medico.tipo if personal_medico else "No especificado"

        # Construir el payload del token con nombre de usuario y tipo de personal
        token_data = {
            "nombre_usuario": usuario.nombre_usuario,
            "contrasena": usuario.contrasena,
            "tipo_personal": tipo_personal
        }

        # Generar el token JWT
        token: str = jwt_config.solicita_token(token_data)

        def serialize_value(value):
            """Convierte fechas y valores no serializables en tipos serializables."""
            if isinstance(value, date):
                return value.isoformat()  # Convierte la fecha a formato de cadena
            elif isinstance(value, Decimal):
                return float(value)  # Convierte Decimal a float
            return value  # Devuelve el valor tal cual si es serializable

        # Construir la respuesta con toda la información
        response_data = {
            "token": token,
            "usuario": {
                "id": db_credentials.id,
                "nombre_usuario": db_credentials.nombre_usuario,
                "correo_electronico": db_credentials.correo_electronico,
                "contrasena": db_credentials.contrasena,
                "numero_telefonico_movil": db_credentials.numero_telefonico_movil,
                "estatus": db_credentials.estatus
            },
            "persona": {
                "id": persona.id,
                "nombre": persona.nombre,
                "primer_apellido": persona.primer_apellido,
                "segundo_apellido": persona.segundo_apellido,
                "curp": persona.curp,
                "genero": persona.genero,
                "grupo_sanguineo": persona.grupo_sanguineo,
                "fecha_nacimiento": serialize_value(persona.fecha_nacimiento)
            } if persona else None,
            "personal_medico": {
                "id": personal_medico.id,
                "cedula_profesional": personal_medico.cedula_profesional,
                "tipo": personal_medico.tipo,
                "especialidad": personal_medico.especialidad,
                "fecha_contratacion": serialize_value(personal_medico.fecha_contratacion),
                "fecha_termino_contrato": serialize_value(personal_medico.fecha_termino_contrato),
                "salario": serialize_value(personal_medico.salario),
                "estatus": personal_medico.estatus
            } if personal_medico else None
        }

        return JSONResponse(status_code=200, content=response_data)

    
    def read_users(self, skip: int = 0, limit: int = 10, db: Session = Depends(databaseMysql.get_db)):
        db_users = usuariosDAO.get_users(db=db, skip=skip, limit=limit)
        return db_users

# Se obtiene la instancia única de UsuariosController
usuarios_controller = UsuariosController()
