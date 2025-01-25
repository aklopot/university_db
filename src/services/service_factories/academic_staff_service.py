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
        self.repository = RepositoryFactory().get_academic_staff_repository()
        super().__init__(AcademicStaffValidator(), self.repository)

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

    def delete_academic_staff(self, academic_staff_id: int) -> None:
        """
        Usuwa pracownika akademickiego.
        """
        try:
            print(f"Próba usunięcia pracownika o ID: {academic_staff_id}")  # Debug log
            self.repository.delete_academic_staff_by_id(academic_staff_id)
        except Exception as e:
            print(f"Błąd w serwisie podczas usuwania pracownika: {e}")
            raise

    def get_by_pesel(self, pesel: str) -> List[AcademicStaff]:
        """
        Pobiera pracowników po numerze PESEL.
        """
        return self.repository.get_by_pesel(pesel)
