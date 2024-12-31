from src.services.service_factories.validators.person_validator import BasePersonValidator
from src.models.universitydb import AcademicStaff
from src.services.exceptions.exceptions import ValidationError

class AcademicStaffValidator(BasePersonValidator[AcademicStaff]):
    """
    Walidator dla pracowników akademickich.
    """
    def _validate_specific(self, academic_staff: AcademicStaff) -> None:
        """
        Wykonuje walidacje specyficzne dla pracownika akademickiego.
        
        Args:
            academic_staff: Obiekt pracownika akademickiego do walidacji
            
        Raises:
            ValidationError: Gdy dane specyficzne dla pracownika akademickiego są nieprawidłowe
        """
        if not academic_staff.position:
            raise ValidationError("Stanowisko jest wymagane")
        if not hasattr(academic_staff.position, 'value'):
            raise ValidationError("Nieprawidłowy format stanowiska") 