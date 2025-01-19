from typing import List
from src.models.universitydb import FieldOfStudy
from src.repositories.repository_factory import RepositoryFactory

class FieldOfStudyService:
    def __init__(self):
        self.repository = RepositoryFactory().get_field_of_study_repository()

    def add_field_of_study(self, field_name: str) -> None:
        """
        Dodaje nowy kierunek studiów.
        """
        field = FieldOfStudy(field_name=field_name)
        self.repository.add_field_of_study(field)

    def update_field_of_study(self, field: FieldOfStudy) -> None:
        """
        Aktualizuje kierunek studiów.
        """
        self.repository.update_field_of_study(field)

    def get_all_fields_of_study(self) -> List[FieldOfStudy]:
        """
        Pobiera listę wszystkich kierunków studiów.
        """
        return self.repository.get_all_fields_of_study()

    def get_field_of_study_by_name(self, name: str) -> FieldOfStudy:
        """
        Pobiera kierunek studiów po nazwie.
        """
        return self.repository.get_field_of_study_by_name(name)

    def delete_field_of_study(self, field_id: int) -> None:
        """
        Usuwa kierunek studiów.
        """
        self.repository.delete_field_of_study_by_id(field_id) 