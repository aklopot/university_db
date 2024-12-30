# pesel.py: Zawiera definicję klasy PESEL, która reprezentuje numer PESEL.
import re
from dataclasses import dataclass
from src.services.exceptions.exceptions import ValidationError

@dataclass(frozen=True)
class PESEL:
    """Value object reprezentujący numer PESEL."""
    value: str

    def __post_init__(self):
        """Walidacja przy tworzeniu obiektu."""
        if not self._validate_format(self.value):
            raise ValidationError("Nieprawidłowy format numeru PESEL. PESEL musi składać się z dokładnie 11 cyfr.")
        if not self._validate_checksum(self.value):
            raise ValidationError("Nieprawidłowa suma kontrolna numeru PESEL.")

    @staticmethod
    def _validate_format(pesel: str) -> bool:
        """Sprawdza, czy PESEL składa się z dokładnie 11 cyfr."""
        return bool(re.match(r"^\d{11}$", pesel))

    @staticmethod
    def _validate_checksum(pesel: str) -> bool:
        """Waliduje sumę kontrolną PESEL."""
        weights = [9, 7, 3, 1, 9, 7, 3, 1, 9, 7]
        checksum = sum(int(pesel[i]) * weights[i] for i in range(10)) % 10
        return checksum == int(pesel[10])

    def __str__(self) -> str:
        return self.value
