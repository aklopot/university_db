# json_repository.py: Zawiera implementacje repozytoriów dla Studentów i Pracowników Akademickich, które korzystają z plików JSON do przechowywania danych.
from typing import List
from src.models.universitydb import Student, AcademicStaff
from src.repositories.base_repositories.base_student_repository import BaseStudentRepository
from src.repositories.base_repositories.base_academic_staff_repository import BaseAcademicStaffRepository
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

# Repozytorium dla pracowników akademickich
class JSONAcademicStaffRepository(BaseAcademicStaffRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def _load_data(self) -> List[AcademicStaff]:
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                return [AcademicStaff(**item) for item in data]
        except FileNotFoundError:
            return []

    def _save_data(self, academic_staff_list: List[AcademicStaff]) -> None:
        with open(self.file_path, 'w') as file:
            json.dump([academic_staff.dict() for academic_staff in academic_staff_list], file)

    def add_academic_staff(self, academic_staff: AcademicStaff) -> None:
        academic_staff_list = self._load_data()
        academic_staff_list.append(academic_staff)
        self._save_data(academic_staff_list)

    def get_all_academic_staff(self) -> List[AcademicStaff]:
        return self._load_data()

    def delete_academic_staff_by_pesel(self, pesel: str) -> None:
        academic_staff_list = self._load_data()
        academic_staff_list = [p for p in academic_staff_list if p.pesel != pesel]
        self._save_data(academic_staff_list)

    def update_academic_staff(self, academic_staff: AcademicStaff) -> None:
        academic_staff_list = self._load_data()
        for i, p in enumerate(academic_staff_list):
            if p.pesel == academic_staff.pesel:
                academic_staff_list[i] = academic_staff
                break
        self._save_data(academic_staff_list)
