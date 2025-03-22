from bson import ObjectId
from src.db.db_mongo import mongodb_instance
from src.schemas.notas_medicas_schemas import NotaMedicaModel
from datetime import datetime, timezone

class NotasMedicasDAO:
    """Clase para gestionar la base de datos de notas médicas en MongoDB (Singleton)."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NotasMedicasDAO, cls).__new__(cls)
            cls._instance.collection = mongodb_instance.db["notas_medicas"]
        return cls._instance

    def crear_nota(self, nota: dict):
        """Inserta una nueva nota médica en la base de datos."""
        resultado = self.collection.insert_one(nota)
        return str(resultado.inserted_id)  # Retorna el ID de la nota creada

    def obtener_nota(self, nota_id: str):
        """Obtiene una nota médica por su ID."""
        return self.collection.find_one({"_id": ObjectId(nota_id)})

    def obtener_todas(self):
        """Obtiene todas las notas médicas."""
        return list(self.collection.find({}))

    def actualizar_nota(self, nota_id: str, nuevos_datos: dict):
        """Actualiza una nota médica por su ID e incluye updatedAt."""
        nuevos_datos["updatedAt"] = datetime.now(timezone.utc)
        resultado = self.collection.update_one(
            {"_id": ObjectId(nota_id)},
            {"$set": nuevos_datos}
        )
        return resultado.modified_count > 0  # True si se modificó algo

    def eliminar_nota(self, nota_id: str):
        """Elimina una nota médica por su ID."""
        resultado = self.collection.delete_one({"_id": ObjectId(nota_id)})
        return resultado.deleted_count > 0  # True si se eliminó algo

# Instancia única del DAO
notasMedicasDAO = NotasMedicasDAO()
