from typing import List, Optional
from src.models.universitydb import FieldOfStudy
from src.repositories.base_repositories.base_field_of_study_repository import BaseFieldOfStudyRepository
import json

class JSONFieldOfStudyRepository(BaseFieldOfStudyRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def _load_data(self) -> List[FieldOfStudy]:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [FieldOfStudy(**item) for item in data.get('fields_of_study', [])]
        except FileNotFoundError:
            # Jeśli plik nie istnieje, tworzymy go z pustą listą
            self._save_data([])
            return []

    def _save_data(self, fields: List[FieldOfStudy]) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump({
                'fields_of_study': [field.dict() for field in fields]
            }, file, indent=4, ensure_ascii=False)

    def add_field_of_study(self, field: FieldOfStudy) -> None:
        fields = self._load_data()
        # Generowanie nowego ID
        max_id = max([f.field_of_study_id for f in fields], default=0)
        field.field_of_study_id = max_id + 1
        fields.append(field)
        self._save_data(fields)

    def get_all_fields_of_study(self) -> List[FieldOfStudy]:
        return self._load_data()

    def get_field_of_study_by_id(self, field_id: int) -> Optional[FieldOfStudy]:
        """
        Pobiera kierunek studiów po ID.
        
        Args:
            field_id (int): ID kierunku studiów
            
        Returns:
            Optional[FieldOfStudy]: Znaleziony kierunek studiów lub None
        """
        fields = self._load_data()
        for field in fields:
            if field.field_of_study_id == field_id:
                return field
        return None

    def get_field_of_study_by_name(self, name: str) -> Optional[FieldOfStudy]:
        fields = self._load_data()
        for field in fields:
            if field.field_name.lower() == name.lower():
                return field
        return None

    def update_field_of_study(self, field: FieldOfStudy) -> None:
        fields = self._load_data()
        for i, f in enumerate(fields):
            if f.field_of_study_id == field.field_of_study_id:
                fields[i] = field
                break
        self._save_data(fields)

    def delete_field_of_study_by_id(self, field_id: int) -> None:
        fields = self._load_data()
        fields = [f for f in fields if f.field_of_study_id != field_id]
        self._save_data(fields) 