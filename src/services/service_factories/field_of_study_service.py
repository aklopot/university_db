from typing import List, Optional
from src.models.universitydb import FieldOfStudy
from src.repositories.repository_factory import RepositoryFactory

class FieldOfStudyService:
    def __init__(self):
        self.repository = RepositoryFactory().get_field_of_study_repository()

    def add_field_of_study(self, name: str) -> None:
        field_of_study = FieldOfStudy(field_name=name)
        self.repository.add_field_of_study(field_of_study)

    def update_field_of_study(self, field_of_study: FieldOfStudy) -> None:
        self.repository.update_field_of_study(field_of_study)

    def get_all_fields_of_study(self) -> List[FieldOfStudy]:
        return self.repository.get_all_fields_of_study()
    
    def get_field_of_study_by_name(self, name: str) -> Optional[FieldOfStudy]:
        return self.repository.get_field_of_study_by_name(name)

    def delete_field_of_study(self, field_of_study_id: int) -> None:
        self.repository.delete_field_of_study_by_id(field_of_study_id) 