from typing import Optional
from src.models.universitydb import Address
from src.services.service_factories.address_service import AddressService
from src.services.service_factories.validators.base_validator import BaseValidator
from src.services.exceptions.exceptions import ValidationError

class AddressValidator(BaseValidator[int]):
    """
    Walidator dla adresu.
    """
    def __init__(self, address_service: AddressService):
        self.address_service = address_service
        
    def validate(self, address_id: int) -> None:
        """
        Sprawdza czy adres istnieje.
        
        Args:
            address_id: ID adresu do zwalidowania
            
        Raises:
            ValidationError: Gdy adres nie istnieje
        """
        address = self.address_service.get_address_by_id(address_id)
        if not address:
            raise ValidationError(f"Address with ID '{address_id}' does not exist.") 