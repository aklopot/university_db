from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.universitydb import FieldOfStudy

class BaseFieldOfStudyRepository(ABC):
    @abstractmethod
    def add_field_of_study(self, field_of_study: FieldOfStudy) -> None:
        pass

    @abstractmethod
    def update_field_of_study(self, field_of_study: FieldOfStudy) -> None:
        pass
    
    @abstractmethod
    def get_all_fields_of_study(self) -> List[FieldOfStudy]:
        pass

    @abstractmethod
    def get_field_of_study_by_name(self, name: str) -> Optional[FieldOfStudy]:
        pass

    @abstractmethod
    def delete_field_of_study_by_id(self, field_of_study_id: int) -> None:
        pass 