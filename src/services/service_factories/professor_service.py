# profesor_service.py: Zawiera definicję klasy ProfessorService, która jest odpowiedzialna za obsługę operacji na profesorach. Klasa ta korzysta z repozytorium profesorów, które jest przekazywane w konstruktorze. ProfessorService udostępnia metody do dodawania, usuwania i aktualizowania profesorów, a także pobierania listy wszystkich profesorów.
from typing import List
from src.models.universitydb import Professor
from src.services.service_factories.base_person_service import BasePersonService
from src.services.service_factories.validators.professor_validator import ProfessorValidator
from src.repositories.repository_factory import RepositoryFactory

class ProfessorService(BasePersonService[Professor]):
    """
    Serwis odpowiedzialny za operacje na profesorach.
    """
    def __init__(self):
        repository = RepositoryFactory().get_professor_repository()
        super().__init__(ProfessorValidator(), repository)

    def add_professor(self, professor: Professor) -> None:
        """
        Dodaje nowego profesora.
        """
        self.add_person(professor)

    def update_professor(self, professor: Professor) -> None:
        """
        Aktualizuje dane profesora.
        """
        self.update_person(professor)

    def get_all_professors(self) -> List[Professor]:
        """
        Pobiera listę wszystkich profesorów.
        """
        return self.get_all()

    def delete_professor(self, pesel: str) -> None:
        """
        Usuwa profesora o podanym numerze PESEL.
        """
        self.delete_by_id(pesel)
