from src.services.validators.person_validator import BasePersonValidator
from src.models.universitydb import Student
from src.services.exceptions.exceptions import ValidationError

class StudentValidator(BasePersonValidator[Student]):
    """
    Walidator dla studentów.
    """
    def _validate_specific(self, student: Student) -> None:
        """
        Wykonuje walidacje specyficzne dla studenta.
        
        Args:
            student: Obiekt studenta do walidacji
            
        Raises:
            ValidationError: Gdy dane specyficzne dla studenta są nieprawidłowe
        """
        if not student.index_number:
            raise ValidationError("Numer indeksu jest wymagany")
        if not student.index_number.isalnum():
            raise ValidationError("Numer indeksu może zawierać tylko litery i cyfry") 