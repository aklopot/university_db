from typing import List, Optional
from src.models.universitydb import Address
from src.repositories.base_repositories.base_address_repository import BaseAddressRepository
import json

class JSONAddressRepository(BaseAddressRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def _load_data(self) -> List[Address]:
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                return [Address(**item) for item in data.get('addresses', [])]
        except FileNotFoundError:
            self._save_data([])
            return []

    def _save_data(self, addresses: List[Address]) -> None:
        with open(self.file_path, 'w') as file:
            json.dump({
                'addresses': [address.dict() for address in addresses]
            }, file, indent=4)

    def add_address(self, address: Address) -> None:
        addresses = self._load_data()
        # Generowanie nowego ID
        max_id = max([a.address_id for a in addresses], default=0)
        address.address_id = max_id + 1
        addresses.append(address)
        self._save_data(addresses)

    def get_all_addresses(self) -> List[Address]:
        return self._load_data()

    def get_address_by_id(self, address_id: int) -> Optional[Address]:
        addresses = self._load_data()
        for address in addresses:
            if address.address_id == address_id:
                return address
        return None

    def update_address(self, address: Address) -> None:
        addresses = self._load_data()
        for i, addr in enumerate(addresses):
            if addr.address_id == address.address_id:
                addresses[i] = address
                break
        self._save_data(addresses)

    def delete_address_by_id(self, address_id: int) -> None:
        addresses = self._load_data()
        addresses = [a for a in addresses if a.address_id != address_id]
        self._save_data(addresses) 