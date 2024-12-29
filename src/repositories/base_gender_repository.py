# base_gender_repository.py: Definiuje interfejs repozytorium płci.
from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.universitydb import Gender

class BaseGenderRepository(ABC):
    @abstractmethod
    def add_gender(self, gender: Gender) -> None:
        pass

    @abstractmethod
    def update_gender(self, gender: Gender) -> None:
        pass
    
    @abstractmethod
    def get_all_genders(self) -> List[Gender]:
        pass

    @abstractmethod
    def get_gender_by_name(self, name: str) -> Optional[Gender]:
        pass

    @abstractmethod
    def delete_gender_by_id(self, gender_id: int) -> None:
        pass
