from pymongo import MongoClient
import os

class MongoDB:
    """Clase Singleton para la conexión a MongoDB."""

    _instance = None

    def __new__(cls):
        """Implementa el patrón Singleton para evitar múltiples conexiones."""
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Inicializa la conexión a MongoDB."""
        mongo_uri = os.getenv("MONGO_URI")  # Usar variable de entorno o default local
        self.client = MongoClient(mongo_uri)
        self.db = self.client.get_database()  # Obtiene la base de datos predeterminada

    def get_database(self, db_name: str):
        """Devuelve una base de datos específica."""
        return self.client[db_name]

# Crear una instancia única
mongodb_instance = MongoDB()


