from src.models.universitydb import Address
from src.repositories.repository_factory import RepositoryFactory
from typing import List, Optional

class AddressService:
    def __init__(self, config):
        self.repository = RepositoryFactory(config).get_address_repository()
    
    def add_address(self, address: Address):
        self.repository.add_address(address)
    
    def update_address(self, address: Address):
        self.repository.update_address(address)
    
    def get_address_by_id(self, address_id: int) -> Optional[Address]:
        return self.repository.get_address_by_id(address_id)
    
    def get_all_addresses(self) -> List[Address]:
        return self.repository.get_all_addresses()
    
    def delete_address(self, address_id: int):
        self.repository.delete_address_by_id(address_id)
