# pesel.py: Zawiera definicję klasy PESEL, która reprezentuje numer PESEL. Klasa ta zawiera metody do walidacji formatu i sumy kontrolnej numeru PESEL.
import re

class PESEL:
    PESEL_REGEX = r"^\d{11}$"

    def __init__(self, pesel: str):
        if not self.validate_format(pesel):
            raise ValueError("Invalid PESEL format. PESEL must be exactly 11 digits.")
        if not self.validate_checksum(pesel):
            raise ValueError("Invalid PESEL checksum.")
        self.pesel = pesel

    @staticmethod
    def validate_format(pesel: str) -> bool:
        """
        Validates that the PESEL consists of exactly 11 digits.
        """
        return bool(re.match(PESEL.PESEL_REGEX, pesel))

    @staticmethod
    def validate_checksum(pesel: str) -> bool:
        """
        Validates the PESEL checksum using the weights and control digit.
        The weights for the first 10 digits are [9, 7, 3, 1, 9, 7, 3, 1, 9, 7].
        """
        weights = [9, 7, 3, 1, 9, 7, 3, 1, 9, 7]
        checksum = sum(int(pesel[i]) * weights[i] for i in range(10)) % 10
        return checksum == int(pesel[10])

    def __str__(self):
        return self.pesel

    def __eq__(self, other):
        if isinstance(other, PESEL):
            return self.pesel == other.pesel
        if isinstance(other, str):
            return self.pesel == other
        return False

    def __hash__(self):
        return hash(self.pesel)
