# students_service.py: Zawiera definicję klasy StudentService, która jest odpowiedzialna za obsługę operacji na studentach. Klasa ta korzysta z repozytorium studentów, które jest przekazywane w konstruktorze. StudentService udostępnia metody do dodawania, usuwania i aktualizowania studentów, a także pobierania listy wszystkich studentów.
from typing import List
from src.models.universitydb import Address, Gender, Student
from src.repositories.repository_factory import RepositoryFactory
from src.services.gender_service import GenderService
from src.services.address_service import AddressService

class StudentService:
    def __init__(self):
        # Tworzymy fabrykę repozytoriów bez przekazywania konfiguracji
        self.repository = RepositoryFactory().get_student_repository()
        self.gender_service = GenderService()
        self.address_service = AddressService()

    def add_student(self, student: Student):
        # Upewnij się, że płeć istnieje
        gender = self.gender_service.get_gender_by_name(student.gender.name)
        if not gender:
            raise ValueError(f"Gender '{student.gender.name}' does not exist.")
        student.gender = gender

        # Upewnij się, że adres istnieje
        address = self.address_service.get_address_by_id(student.address.address_id)
        if not address:
            raise ValueError(f"Address with ID '{student.address.address_id}' does not exist.")
        student.address = address

        # Dodaj studenta do bazy danych
        self.repository.add_student(student)

    def get_all_students(self) -> List[Student]:
        return self.repository.get_all_students()

    def delete_student(self, index_number: str):
        self.repository.delete_student_by_index(index_number)

    def update_student(self, student: Student):
        self.repository.update_student(student)
