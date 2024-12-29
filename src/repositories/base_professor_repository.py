# base_professor_repository.py: Jest klasą abstrakcyjną, która definiuje metody, które muszą zostać zaimplementowane przez dowolną klasę, która z niej dziedziczy. Definiuje metody, które będą używane do interakcji z magazynem danych.
from abc import ABC, abstractmethod
from typing import List
from src.models.universitydb import Professor

class BaseProfessorRepository(ABC):
    @abstractmethod
    def add_professor(self, professor: Professor) -> None:
        """
        Add a new professor to the data store.
        """
        pass

    @abstractmethod
    def get_all_professors(self) -> List[Professor]:
        """
        Retrieve all professors from the data store.
        """
        pass

    @abstractmethod
    def delete_professor_by_pesel(self, pesel: str) -> None:
        """
        Delete a professor using their PESEL number.
        """
        pass

    @abstractmethod
    def update_professor(self, professor: Professor) -> None:
        """
        Update an existing professor's information.
        """
        pass
