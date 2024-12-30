# base_student_repository.py: Jest klasą abstrakcyjną, która definiuje metody, które muszą zostać zaimplementowane przez dowolną klasę, która z niej dziedziczy. Definiuje metody, które będą używane do interakcji z magazynem danych.
from abc import ABC, abstractmethod
from typing import List
from src.models.universitydb import Student
from src.repositories.base_person_repository import BasePersonRepository

class BaseStudentRepository(BasePersonRepository[Student]):
    """
    Interfejs repozytorium dla studentów.
    """
    def add(self, student: Student) -> None:
        return self.add_student(student)

    def update(self, student: Student) -> None:
        return self.update_student(student)

    def get_all(self) -> List[Student]:
        return self.get_all_students()

    def delete_by_id(self, identifier: str) -> None:
        return self.delete_student_by_index(identifier)

    @abstractmethod
    def add_student(self, student: Student) -> None:
        """
        Add a new student to the data store.
        """
        pass

    @abstractmethod
    def update_student(self, student: Student) -> None:
        """
        Update an existing student's information.
        """
        pass

    @abstractmethod
    def get_all_students(self) -> List[Student]:
        """
        Retrieve all students from the data store.
        """
        pass

    @abstractmethod
    def delete_student_by_index(self, index_number: str) -> None:
        """
        Delete a student using their index number.
        """
        pass
