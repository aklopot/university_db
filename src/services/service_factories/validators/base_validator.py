from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic

T = TypeVar('T')

class BaseValidator(Generic[T], ABC):
    """
    Bazowa klasa abstrakcyjna dla wszystkich walidatorów.
    """
    @abstractmethod
    def validate(self, value: T) -> None:
        """
        Waliduje wartość.
        
        Args:
            value: Wartość do zwalidowania
            
        Raises:
            ValidationError: Gdy walidacja się nie powiedzie
        """
        pass 