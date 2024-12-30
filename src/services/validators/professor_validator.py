from src.services.validators.person_validator import BasePersonValidator
from src.models.universitydb import Professor
from src.services.exceptions.exceptions import ValidationError

class ProfessorValidator(BasePersonValidator[Professor]):
    """
    Walidator dla profesorów.
    """
    def _validate_specific(self, professor: Professor) -> None:
        """
        Wykonuje walidacje specyficzne dla profesora.
        
        Args:
            professor: Obiekt profesora do walidacji
            
        Raises:
            ValidationError: Gdy dane specyficzne dla profesora są nieprawidłowe
        """
        if not professor.position:
            raise ValidationError("Stanowisko jest wymagane")
        if not hasattr(professor.position, 'value'):
            raise ValidationError("Nieprawidłowy format stanowiska") 