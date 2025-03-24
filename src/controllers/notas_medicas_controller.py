from fastapi import HTTPException
from fastapi.responses import JSONResponse
from bson import ObjectId
from src.dao.notas_medicas_dao import notasMedicasDAO
from src.schemas.notas_medicas_schemas import NotaMedicaCreate, NotaMedicaUpdate

class NotasMedicasController:
    """Controlador de notas médicas (Singleton)."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NotasMedicasController, cls).__new__(cls)
        return cls._instance

    def crear_nota(self, nota: NotaMedicaCreate):
        """Crea una nueva nota médica."""
        nota_dict = nota.dict(by_alias=True)
        nota_id = notasMedicasDAO.crear_nota(nota_dict)
        return JSONResponse(content={"message": "Nota creada", "id": nota_id}, status_code=201)

    def obtener_nota(self, nota_id: str):
        """Obtiene una nota médica por ID."""
        nota = notasMedicasDAO.obtener_nota(nota_id)
        if not nota:
            raise HTTPException(status_code=404, detail="Nota no encontrada")
        return nota

    def obtener_todas(self):
        """Obtiene todas las notas médicas."""
        return notasMedicasDAO.obtener_todas()

    def actualizar_nota(self, nota_id: str, nuevos_datos: dict):
        """Actualiza una nota médica."""
        if not notasMedicasDAO.actualizar_nota(nota_id, nuevos_datos):
            raise HTTPException(status_code=404, detail="No se pudo actualizar la nota")
        return {"message": "Nota actualizada"}

    def eliminar_nota(self, nota_id: str):
        """Elimina una nota médica."""
        if not notasMedicasDAO.eliminar_nota(nota_id):
            raise HTTPException(status_code=404, detail="Nota no encontrada")
        return {"message": "Nota eliminada"}

# Instancia única del controlador
notasMedicasController = NotasMedicasController()

