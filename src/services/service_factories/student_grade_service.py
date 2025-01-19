from typing import List
from src.models.universitydb import StudentGrade
from src.repositories.repository_factory import RepositoryFactory

class StudentGradeService:
    def __init__(self):
        self.repository = RepositoryFactory().get_student_grade_repository()

    def add_student_grade(self, grade: StudentGrade) -> None:
        """
        Dodaje nową ocenę studenta.
        """
        self.repository.add_student_grade(grade)

    def update_student_grade(self, grade: StudentGrade) -> None:
        """
        Aktualizuje ocenę studenta.
        """
        self.repository.update_student_grade(grade)

    def get_student_grades(self, student_id: int) -> List[StudentGrade]:
        """
        Pobiera wszystkie oceny danego studenta.
        """
        return self.repository.get_student_grades(student_id)

    def delete_student_grade(self, grade_id: int) -> None:
        """
        Usuwa ocenę studenta.
        """
        self.repository.delete_student_grade_by_id(grade_id) 