import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class DatabaseMySQL:
    _instance = None  # Variable de clase para la instancia única

    def __new__(cls):
        """Implementa el patrón Singleton para asegurar una única instancia."""
        if cls._instance is None:
            cls._instance = super(DatabaseMySQL, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Inicializa la conexión a la base de datos usando variables de entorno."""
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")

        self.engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}")
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()

    def get_session(self):
        """Retorna la sesión de base de datos"""
        return self.SessionLocal()
    
    def get_base(self):
        """Retorna la base de datos declarativa"""
        return self.Base
    
    def get_engine(self):
        """Retorna el engine"""
        return self.engine
    
    def get_db(self):
        """Dependencia para FastAPI que maneja sesiones de DB"""
        session = self.get_session()
        try:
            yield session
        finally:
            session.close()

# Crear la instancia única de la base de datos
databaseMysql = DatabaseMySQL()
