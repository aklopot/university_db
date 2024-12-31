# academic_staff_service.py: Zawiera definicję klasy AcademicStaffService, która jest odpowiedzialna za obsługę operacji na pracownikach akademickich. Klasa ta korzysta z repozytorium pracowników akademickich, które jest przekazywane w konstruktorze. AcademicStaffService udostępnia metody do dodawania, usuwania i aktualizowania pracowników akademickich, a także pobierania listy wszystkich pracowników akademickich.
from typing import List
from src.models.universitydb import AcademicStaff
from src.services.service_factories.base_person_service import BasePersonService
from src.services.service_factories.validators.academic_staff_validator import AcademicStaffValidator
from src.repositories.repository_factory import RepositoryFactory

class AcademicStaffService(BasePersonService[AcademicStaff]):
    """
    Serwis odpowiedzialny za operacje na pracownikach akademickich.
    """
    def __init__(self):
        repository = RepositoryFactory().get_academic_staff_repository()
        super().__init__(AcademicStaffValidator(), repository)

    def add_academic_staff(self, academic_staff: AcademicStaff) -> None:
        """
        Dodaje nowego pracownika akademickiego.
        """
        self.add_person(academic_staff)

    def update_academic_staff(self, academic_staff: AcademicStaff) -> None:
        """
        Aktualizuje dane pracownika akademickiego.
        """
        self.update_person(academic_staff)

    def get_all_academic_staff(self) -> List[AcademicStaff]:
        """
        Pobiera listę wszystkich pracowników akademickich.
        """
        return self.get_all()

    def delete_academic_staff(self, pesel: str) -> None:
        """
        Usuwa pracownika akademickiego o podanym numerze PESEL.
        """
        self.delete_by_id(pesel)
