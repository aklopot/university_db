from typing import List, Optional
from src.models.universitydb import Student
from src.repositories.base_repositories.base_student_repository import BaseStudentRepository
import json


# Repozytorium dla Studentów
class JSONStudentRepository(BaseStudentRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def _load_data(self) -> List[Student]:
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                return [Student(**item) for item in data]
        except FileNotFoundError:
            return []

    def _save_data(self, students: List[Student]) -> None:
        with open(self.file_path, 'w') as file:
            json.dump([student.dict() for student in students], file, indent=4)

    def add_student(self, student: Student) -> None:
        students = self._load_data()
        students.append(student)
        self._save_data(students)

    def get_all_students(self) -> List[Student]:
        return self._load_data()

    def delete_student_by_index(self, index_number: str) -> None:
        students = self._load_data()
        students = [s for s in students if s.index_number != index_number]
        self._save_data(students)

    def update_student(self, student: Student) -> None:
        students = self._load_data()
        for i, s in enumerate(students):
            if s.index_number == student.index_number:
                students[i] = student
                break
        self._save_data(students)

    def get_by_last_name(self, last_name: str) -> List[Student]:
        students = self._load_data()
        return [s for s in students if s.last_name.lower().startswith(last_name.lower())]

    def get_by_pesel(self, pesel: str) -> List[Student]:
        students = self._load_data()
        return [s for s in students if s.pesel.startswith(pesel)]

    def get_all_students_sorted_by_name(self) -> List[Student]:
        students = self._load_data()
        return sorted(students, key=lambda x: (x.last_name, x.first_name))

    def get_all_students_sorted_by_pesel(self) -> List[Student]:
        students = self._load_data()
        return sorted(students, key=lambda x: x.pesel)
