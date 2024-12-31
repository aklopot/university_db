from abc import abstractmethod
from typing import TypeVar, Generic
from src.services.service_factories.validators.base_validator import BaseValidator
from src.models.pesel import PESEL
from src.services.exceptions.exceptions import ValidationError

T = TypeVar('T')

class BasePersonValidator(BaseValidator[T], Generic[T]):
    """
    Bazowy walidator dla osób (studentów i profesorów).
    """
    def validate(self, person: T) -> None:
        """
        Wykonuje podstawową walidację osoby.
        
        Args:
            person: Obiekt osoby do walidacji
            
        Raises:
            ValidationError: Gdy dane osoby są nieprawidłowe
        """
        if not person.first_name:
            raise ValidationError("Imię jest wymagane")
        if not person.last_name:
            raise ValidationError("Nazwisko jest wymagane")
            
        # Walidacja PESEL przy użyciu value objectu
        try:
            PESEL(person.pesel)
        except ValidationError as e:
            raise ValidationError(f"Nieprawidłowy numer PESEL: {str(e)}")

        # Walidacja specyficzna dla konkretnego typu osoby
        self._validate_specific(person)


    @abstractmethod
    def _validate_specific(self, person: T) -> None:
        """
        Metoda do nadpisania przez klasy pochodne.
        Wykonuje walidacje specyficzne dla danego typu osoby.
        """
        pass 