# base_student_repository.py: Jest klasą abstrakcyjną, która definiuje metody, które muszą zostać zaimplementowane przez dowolną klasę, która z niej dziedziczy. Definiuje metody, które będą używane do interakcji z magazynem danych.
from abc import ABC, abstractmethod
from typing import List
from src.models.universitydb import Student

class BaseStudentRepository(ABC):
    @abstractmethod
    def add_student(self, student: Student) -> None:
        """
        Add a new student to the data store.
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

    @abstractmethod
    def update_student(self, student: Student) -> None:
        """
        Update an existing student's information.
        """
        pass
