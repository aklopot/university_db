from typing import Optional
from src.models.universitydb import Gender
from src.services.gender_service import GenderService
from src.services.validators.base_validator import BaseValidator
from src.services.exceptions.exceptions import ValidationError

class GenderValidator(BaseValidator[str]):
    """
    Walidator dla płci.
    """
    def __init__(self, gender_service: GenderService):
        self.gender_service = gender_service
        
    def validate(self, gender_name: str) -> None:
        """
        Sprawdza czy płeć istnieje.
        
        Args:
            gender_name: Nazwa płci do zwalidowania
            
        Raises:
            ValidationError: Gdy płeć nie istnieje
        """
        gender = self.gender_service.get_gender_by_name(gender_name)
        if not gender:
            raise ValidationError(f"Gender '{gender_name}' does not exist.") 