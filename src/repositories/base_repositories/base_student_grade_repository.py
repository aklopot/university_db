from abc import ABC, abstractmethod
from typing import List
from src.models.universitydb import StudentGrade

class BaseStudentGradeRepository(ABC):
    @abstractmethod
    def add_student_grade(self, grade: StudentGrade) -> None:
        pass

    @abstractmethod
    def update_student_grade(self, grade: StudentGrade) -> None:
        pass
    
    @abstractmethod
    def get_student_grades(self, student_id: int) -> List[StudentGrade]:
        pass

    @abstractmethod
    def delete_student_grade_by_id(self, grade_id: int) -> None:
        pass 