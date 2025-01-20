from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic

T = TypeVar('T')

class BasePersonRepository(Generic[T], ABC):
    """
    Bazowy interfejs dla repozytoriów przechowujących dane osób.
    """
    @abstractmethod
    def add(self, person: T) -> None:
        """
        Dodaje nową osobę do repozytorium.
        """
        pass

    @abstractmethod
    def update(self, person: T) -> None:
        """
        Aktualizuje dane osoby w repozytorium.
        """
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        """
        Pobiera wszystkie osoby z repozytorium.
        """
        pass

    @abstractmethod
    def delete_by_id(self, identifier: str) -> None:
        """
        Usuwa osobę o podanym identyfikatorze.
        """
        pass

    @abstractmethod
    def get_by_last_name(self, last_name: str) -> List[T]:
        """
        Pobiera wszystkie osoby o podanym nazwisku.
        
        Args:
            last_name (str): Nazwisko do wyszukania
            
        Returns:
            List[T]: Lista znalezionych osób
        """
        pass 