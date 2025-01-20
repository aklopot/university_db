from typing import Generic, TypeVar, List
from src.services.service_factories.validators.base_validator import BaseValidator
from src.repositories.base_repositories.base_person_repository import BasePersonRepository
from src.services.exceptions.exceptions import ValidationError

T = TypeVar('T')

class BasePersonService(Generic[T]):
    """
    Bazowa klasa serwisu dla operacji na osobach (np. studentach, pracownikach akademickich).
    Implementuje wspólną logikę dla wszystkich typów osób.
    """
    def __init__(self, validator: BaseValidator[T], repository: BasePersonRepository[T]):
        self.validator = validator
        self.repository = repository

    def add_person(self, person: T) -> None:
        """
        Dodaje nową osobę po walidacji danych.
        
        Args:
            person: Obiekt osoby do dodania
            
        Raises:
            ValidationError: Gdy dane osoby są nieprawidłowe
        """
        try:
            self.validator.validate(person)
            self.repository.add(person)
        except Exception as e:
            raise ValidationError(f"Błąd podczas dodawania: {str(e)}")

    def update_person(self, person: T) -> None:
        """
        Aktualizuje dane osoby po walidacji.
        
        Args:
            person: Obiekt osoby do aktualizacji
            
        Raises:
            ValidationError: Gdy dane osoby są nieprawidłowe
        """
        try:
            self.validator.validate(person)
            self.repository.update(person)
        except Exception as e:
            raise ValidationError(f"Błąd podczas aktualizacji: {str(e)}")

    def get_all(self) -> List[T]:
        """
        Pobiera listę wszystkich osób.
        
        Returns:
            Lista obiektów osób
        """
        return self.repository.get_all()

    def delete_by_id(self, identifier: str) -> None:
        """
        Usuwa osobę o podanym identyfikatorze.
        
        Args:
            identifier: Identyfikator osoby do usunięcia
        """
        self.repository.delete_by_id(identifier)

    def get_by_last_name(self, last_name: str) -> List[T]:
        """
        Pobiera listę osób o podanym nazwisku.
        
        Args:
            last_name (str): Nazwisko do wyszukania
            
        Returns:
            List[T]: Lista znalezionych osób
        """
        try:
            return self.repository.get_by_last_name(last_name)
        except Exception as e:
            raise ValidationError(f"Błąd podczas wyszukiwania po nazwisku: {str(e)}") 