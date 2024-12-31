# json_repository.py: Zawiera implementacje repozytoriów dla Studentów i Profesorów, które korzystają z plików JSON do przechowywania danych.
from typing import List
from src.models.universitydb import Student, Professor
from src.repositories.base_repositories.base_student_repository import BaseStudentRepository
from src.repositories.base_repositories.base_professor_repository import BaseProfessorRepository
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
            json.dump([student.dict() for student in students], file)

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

# Repozytorium dla Profesorów
class JSONProfessorRepository(BaseProfessorRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def _load_data(self) -> List[Professor]:
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                return [Professor(**item) for item in data]
        except FileNotFoundError:
            return []

    def _save_data(self, professors: List[Professor]) -> None:
        with open(self.file_path, 'w') as file:
            json.dump([professor.dict() for professor in professors], file)

    def add_professor(self, professor: Professor) -> None:
        professors = self._load_data()
        professors.append(professor)
        self._save_data(professors)

    def get_all_professors(self) -> List[Professor]:
        return self._load_data()

    def delete_professor_by_pesel(self, pesel: str) -> None:
        professors = self._load_data()
        professors = [p for p in professors if p.pesel != pesel]
        self._save_data(professors)

    def update_professor(self, professor: Professor) -> None:
        professors = self._load_data()
        for i, p in enumerate(professors):
            if p.pesel == professor.pesel:
                professors[i] = professor
                break
        self._save_data(professors)
