# profesor_service.py: Zawiera definicję klasy ProfessorService, która jest odpowiedzialna za obsługę operacji na profesorach. Klasa ta korzysta z repozytorium profesorów, które jest przekazywane w konstruktorze. ProfessorService udostępnia metody do dodawania, usuwania i aktualizowania profesorów, a także pobierania listy wszystkich profesorów.
from src.models.universitydb import Professor
from src.repositories.repository_factory import RepositoryFactory
from src.services.gender_service import GenderService
from src.services.address_service import AddressService
from typing import List

class ProfessorService:
    def __init__(self):
        self.repository = RepositoryFactory().get_professor_repository()
        self.gender_service = GenderService()
        self.address_service = AddressService()
        
    def add_professor(self, professor: Professor):
        # Upewnij się, że płeć istnieje
        gender = self.gender_service.get_gender_by_name(professor.gender.name)
        if not gender:
            raise ValueError(f"Gender '{professor.gender.name}' does not exist.")
        professor.gender = gender
        
        # Upewnij się, że adres istnieje
        address = self.address_service.get_address_by_id(professor.address.address_id)
        if not address:
            raise ValueError(f"Address with ID '{professor.address.address_id}' does not exist.")
        professor.address = address
        
        self.repository.add_professor(professor)
        
    def update_professor(self, professor: Professor):
        # Podobnie jak w add_professor
        gender = self.gender_service.get_gender_by_name(professor.gender.name)
        if not gender:
            raise ValueError(f"Gender '{professor.gender.name}' does not exist.")
        professor.gender = gender
        
        address = self.address_service.get_address_by_id(professor.address.address_id)
        if not address:
            raise ValueError(f"Address with ID '{professor.address.address_id}' does not exist.")
        professor.address = address
        
        self.repository.update_professor(professor)
        
    def get_all_professors(self) -> List[Professor]:
        return self.repository.get_all_professors()
    
    def delete_professor(self, pesel: str):
        self.repository.delete_professor_by_pesel(pesel)
