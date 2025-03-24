from src.models.areas_medicas_model import AreaMedica
from src.models.departamentos_model import Departamento
from src.models.personal_medico_model import PersonalMedico
from src.models.personas_model import Persona
from src.models.usuarios_model import Usuario
from sqlalchemy.orm import relationship

# Definir relaciones entre modelos



# Exportar modelos
__all__ = ["AreaMedica", "Departamento", "PersonalMedico", "Persona", "Usuario"]
