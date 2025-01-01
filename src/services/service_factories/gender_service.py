# gender_service.py: Zawiera definicję klasy GenderService, która obsługuje operacje na płciach.
from src.models.universitydb import Gender
from src.repositories.repository_factory import RepositoryFactory
from typing import List, Optional

class GenderService:
    def __init__(self):
        self.repository = RepositoryFactory().get_gender_repository()

    def add_gender(self, name: str):
        gender = Gender(gender_name=name)
        self.repository.add_gender(gender)

    def update_gender(self, gender: Gender):
        self.repository.update_gender(gender)

    def get_all_genders(self) -> List[Gender]:
        return self.repository.get_all_genders()
    
    def get_gender_by_name(self, name: str) -> Optional[Gender]:
        return self.repository.get_gender_by_name(name)

    def delete_gender(self, gender_id: int):
        self.repository.delete_gender_by_id(gender_id)
