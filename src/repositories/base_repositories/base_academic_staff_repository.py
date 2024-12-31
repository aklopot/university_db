# base_academic_staff_repository.py: Jest klasą abstrakcyjną, która definiuje metody, które muszą zostać zaimplementowane przez dowolną klasę, która z niej dziedziczy. Definiuje metody, które będą używane do interakcji z magazynem danych.
from abc import abstractmethod
from typing import List
from src.models.universitydb import AcademicStaff
from src.repositories.base_repositories.base_person_repository import BasePersonRepository

class BaseAcademicStaffRepository(BasePersonRepository[AcademicStaff]):
    """
    Interfejs repozytorium dla pracowników akademickich.
    """
    def add(self, academic_staff: AcademicStaff) -> None:
        return self.add_academic_staff(academic_staff)

    def update(self, academic_staff: AcademicStaff) -> None:
        return self.update_academic_staff(academic_staff)

    def get_all(self) -> List[AcademicStaff]:
        return self.get_all_academic_staff()

    def delete_by_id(self, identifier: str) -> None:
        return self.delete_academic_staff_by_pesel(identifier)

    @abstractmethod
    def add_academic_staff(self, academic_staff: AcademicStaff) -> None:
        pass

    @abstractmethod
    def update_academic_staff(self, academic_staff: AcademicStaff) -> None:
        pass

    @abstractmethod
    def get_all_academic_staff(self) -> List[AcademicStaff]:
        pass

    @abstractmethod
    def delete_academic_staff_by_pesel(self, pesel: str) -> None:
        pass
