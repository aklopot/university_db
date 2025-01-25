from typing import List, Optional
from src.models.universitydb import StudentGrade
from src.repositories.base_repositories.base_student_grade_repository import BaseStudentGradeRepository
import json

class JSONStudentGradeRepository(BaseStudentGradeRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def _load_data(self) -> List[StudentGrade]:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [StudentGrade(**item) for item in data.get('grades', [])]
        except FileNotFoundError:
            self._save_data([])
            return []

    def _save_data(self, grades: List[StudentGrade]) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump({
                'grades': [grade.dict() for grade in grades]
            }, file, indent=4, ensure_ascii=False)

    def add_student_grade(self, grade: StudentGrade) -> None:
        grades = self._load_data()
        max_id = max([g.grade_id for g in grades], default=0)
        grade.grade_id = max_id + 1
        grades.append(grade)
        self._save_data(grades)

    def get_all_student_grades(self) -> List[StudentGrade]:
        return self._load_data()

    def get_student_grades(self, student_id: int) -> List[StudentGrade]:
        """
        Pobiera wszystkie oceny dla danego studenta.
        
        Args:
            student_id (int): ID studenta
            
        Returns:
            List[StudentGrade]: Lista ocen studenta
        """
        grades = self._load_data()
        return [grade for grade in grades if grade.student_id == student_id]

    def get_student_grade_by_id(self, grade_id: int) -> Optional[StudentGrade]:
        grades = self._load_data()
        for grade in grades:
            if grade.grade_id == grade_id:
                return grade
        return None

    def update_student_grade(self, grade: StudentGrade) -> None:
        grades = self._load_data()
        for i, g in enumerate(grades):
            if g.grade_id == grade.grade_id:
                grades[i] = grade
                break
        self._save_data(grades)

    def delete_student_grade_by_id(self, grade_id: int) -> None:
        grades = self._load_data()
        grades = [g for g in grades if g.grade_id != grade_id]
        self._save_data(grades)

    def add(self, grade: StudentGrade) -> None:
        self.add_student_grade(grade)

    def update(self, grade: StudentGrade) -> None:
        self.update_student_grade(grade)

    def get_all(self) -> List[StudentGrade]:
        return self.get_all_student_grades()

    def delete_by_id(self, grade_id: int) -> None:
        self.delete_student_grade_by_id(grade_id) 