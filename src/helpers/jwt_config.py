import jwt
import os
from dotenv import load_dotenv
from typing import Dict

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class JWTConfig:
    """Clase Singleton para manejar la generación y validación de tokens JWT."""
    
    _instance = None  # Variable de clase para almacenar la única instancia

    def __new__(cls):
        """Implementa el patrón Singleton asegurando una única instancia."""
        if cls._instance is None:
            cls._instance = super(JWTConfig, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Inicializa la configuración del JWT obteniendo valores desde el .env"""
        self.secret_key = os.getenv("JWT_SECRET_KEY")
        self.algorithm = os.getenv("JWT_ALGORITHM")

    def solicita_token(self, dato: Dict) -> str:
        """Genera un token JWT con los datos proporcionados."""
        return jwt.encode(payload=dato, key=self.secret_key, algorithm=self.algorithm)

    def valida_token(self, token: str) -> Dict:
        """Valida y decodifica un token JWT."""
        return jwt.decode(token, key=self.secret_key, algorithms=[self.algorithm])

# Crear la instancia única
jwt_config = JWTConfig()
