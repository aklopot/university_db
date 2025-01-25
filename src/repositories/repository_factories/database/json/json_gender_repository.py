from typing import List, Optional
from src.models.universitydb import Gender
from src.repositories.base_repositories.base_gender_repository import BaseGenderRepository
import json

class JSONGenderRepository(BaseGenderRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def _load_data(self) -> List[Gender]:
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                return [Gender(**item) for item in data.get('genders', [])]
        except FileNotFoundError:
            self._save_data([
                Gender(gender_id=1, name="Mężczyzna"),
                Gender(gender_id=2, name="Kobieta")
            ])
            return self._load_data()

    def _save_data(self, genders: List[Gender]) -> None:
        with open(self.file_path, 'w') as file:
            json.dump({
                'genders': [gender.dict() for gender in genders]
            }, file, indent=4)

    def add_gender(self, gender: Gender) -> None:
        genders = self._load_data()
        # Generowanie nowego ID
        max_id = max([g.gender_id for g in genders], default=0)
        gender.gender_id = max_id + 1
        genders.append(gender)
        self._save_data(genders)

    def update_gender(self, gender: Gender) -> None:
        genders = self._load_data()
        for i, g in enumerate(genders):
            if g.gender_id == gender.gender_id:
                genders[i] = gender
                break
        self._save_data(genders)

    def get_all_genders(self) -> List[Gender]:
        return self._load_data()

    def get_gender_by_name(self, name: str) -> Optional[Gender]:
        genders = self._load_data()
        for gender in genders:
            if gender.name == name:
                return gender
        return None

    def delete_gender_by_id(self, gender_id: int) -> None:
        genders = self._load_data()
        genders = [g for g in genders if g.gender_id != gender_id]
        self._save_data(genders)

    def get_gender_by_id(self, gender_id: int) -> Gender:
        genders = self._load_data()
        for gender in genders:
            if gender.gender_id == gender_id:
                return gender
        return None 