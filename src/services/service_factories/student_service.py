# students_service.py: Zawiera definicję klasy StudentService, która jest odpowiedzialna za obsługę operacji na studentach. Klasa ta korzysta z repozytorium studentów, które jest przekazywane w konstruktorze. StudentService udostępnia metody do dodawania, usuwania i aktualizowania studentów, a także pobierania listy wszystkich studentów.
from typing import List
from src.models.universitydb import Student
from src.services.service_factories.base_person_service import BasePersonService
from src.services.service_factories.validators.student_validator import StudentValidator
from src.repositories.repository_factory import RepositoryFactory

class StudentService(BasePersonService[Student]):
    """
    Serwis odpowiedzialny za operacje na studentach.
    """
    def __init__(self):
        repository = RepositoryFactory().get_student_repository()
        super().__init__(StudentValidator(), repository)

    def add_student(self, student: Student) -> None:
        """
        Dodaje nowego studenta.
        """
        self.add_person(student)

    def update_student(self, student: Student) -> None:
        """
        Aktualizuje dane studenta.
        """
        self.update_person(student)

    def get_all_students(self) -> List[Student]:
        """
        Pobiera listę wszystkich studentów.
        """
        return self.get_all()

    def delete_student(self, index_number: str) -> None:
        """
        Usuwa studenta o podanym numerze indeksu.
        """
        self.delete_by_id(index_number)

    def get_by_pesel(self, pesel: str) -> List[Student]:
        """
        Pobiera studentów po numerze PESEL.
        """
        return self.repository.get_by_pesel(pesel)
