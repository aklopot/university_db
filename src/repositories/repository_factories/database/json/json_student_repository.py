from typing import List, Optional
from src.models.universitydb import Student, Address
from src.repositories.base_repositories.base_student_repository import BaseStudentRepository
import json


# Repozytorium dla Studentów
class JSONStudentRepository(BaseStudentRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def _load_data(self) -> List[Student]:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                # Sprawdzamy format danych
                if isinstance(data, list):
                    students_data = data
                else:
                    students_data = data.get('students', [])
                return [self._create_student_object(item) for item in students_data]
        except FileNotFoundError:
            # Inicjalizujemy plik z pustą listą studentów
            self._save_data([])
            return []

    def _create_student_object(self, data: dict) -> Student:
        # Tworzymy podstawowy obiekt Student z danymi z JSON
        student = Student(
            student_id=data.get('student_id'),
            index_number=data.get('index_number'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            pesel=data.get('pesel'),
            gender_id=data.get('gender_id'),
            field_of_study_id=data.get('field_of_study_id'),
            address_id=data.get('address_id')
        )
        
        return student

    def _save_data(self, students: List[Student]) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json_data = [
                {
                    'student_id': student.student_id,
                    'index_number': student.index_number,
                    'first_name': student.first_name,
                    'last_name': student.last_name,
                    'pesel': student.pesel,
                    'gender_id': student.gender_id,
                    'field_of_study_id': student.field_of_study_id,
                    'address_id': student.address_id
                }
                for student in students
            ]
            json.dump(json_data, file, indent=4, ensure_ascii=False)

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
