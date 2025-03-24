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
        nota = notasMedicasDAO.obtener_nota(nota_id)
        if not nota:
            raise HTTPException(status_code=404, detail="Nota no encontrada")
    
        # Convertir el _id a string
        nota["_id"] = str(nota["_id"])
        return nota


    def obtener_todas(self):
        """Obtiene todas las notas médicas."""
        notas = notasMedicasDAO.obtener_todas()

        # Convertir ObjectId a str en cada documento
        for nota in notas:
            nota["_id"] = str(nota["_id"])

        return notas


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
    
    def agrupadas_por_diagnostico(self):
        """Obtiene las notas médicas agrupadas por diagnóstico y fecha."""
        try:
            agrupadas = notasMedicasDAO.agrupacion_por_diagnostico_y_fecha()
            return agrupadas
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener notas agrupadas: {str(e)}")


# Instancia única del controlador
notasMedicasController = NotasMedicasController()

