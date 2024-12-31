# base_professor_repository.py: Jest klasą abstrakcyjną, która definiuje metody, które muszą zostać zaimplementowane przez dowolną klasę, która z niej dziedziczy. Definiuje metody, które będą używane do interakcji z magazynem danych.
from abc import ABC, abstractmethod
from typing import List
from src.models.universitydb import Professor
from src.repositories.base_repositories.base_person_repository import BasePersonRepository

class BaseProfessorRepository(BasePersonRepository[Professor]):
    """
    Interfejs repozytorium dla profesorów.
    """
    def add(self, professor: Professor) -> None:
        return self.add_professor(professor)

    def update(self, professor: Professor) -> None:
        return self.update_professor(professor)

    def get_all(self) -> List[Professor]:
        return self.get_all_professors()

    def delete_by_id(self, identifier: str) -> None:
        return self.delete_professor_by_pesel(identifier)

    @abstractmethod
    def add_professor(self, professor: Professor) -> None:
        pass

    @abstractmethod
    def update_professor(self, professor: Professor) -> None:
        pass

    @abstractmethod
    def get_all_professors(self) -> List[Professor]:
        pass

    @abstractmethod
    def delete_professor_by_pesel(self, pesel: str) -> None:
        pass
