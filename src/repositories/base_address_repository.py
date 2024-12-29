from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.universitydb import Address

class BaseAddressRepository(ABC):
    @abstractmethod
    def add_address(self, address: Address) -> None:
        pass
    
    @abstractmethod
    def update_address(self, address: Address) -> None:
        pass
    
    @abstractmethod
    def get_address_by_id(self, address_id: int) -> Optional[Address]:
        pass
    
    @abstractmethod
    def get_all_addresses(self) -> List[Address]:
        pass
    
    @abstractmethod
    def delete_address_by_id(self, address_id: int) -> None:
        pass
