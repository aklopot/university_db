from sqlalchemy.orm import joinedload
from src.models.universitydb import StudentGrade, Student, AcademicCourse

class StudentGradeService:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def get_student_grades(self, student_id: int) -> list[StudentGrade]:
        with self.session_factory() as session:
            # Dodajemy eager loading dla potrzebnych relacji
            grades = session.query(StudentGrade)\
                .options(
                    joinedload(StudentGrade.academic_course),
                    joinedload(StudentGrade.student).joinedload(Student.field_of_study)
                )\
                .filter(StudentGrade.student_id == student_id)\
                .all()
            
            # Wymuszamy załadowanie relacji przed zamknięciem sesji
            for grade in grades:
                if grade.student:
                    _ = grade.student.field_of_study
                if grade.academic_course:
                    _ = grade.academic_course.field_of_study
            
            return grades

    def get_grade(self, grade_id: int) -> StudentGrade:
        with self.session_factory() as session:
            # Dodajemy eager loading dla potrzebnych relacji
            grade = session.query(StudentGrade)\
                .options(
                    joinedload(StudentGrade.academic_course),
                    joinedload(StudentGrade.student).joinedload(Student.field_of_study)
                )\
                .filter(StudentGrade.student_grade_id == grade_id)\
                .first()
            
            if grade:
                # Wymuszamy załadowanie relacji przed zamknięciem sesji
                if grade.student:
                    _ = grade.student.field_of_study
                if grade.academic_course:
                    _ = grade.academic_course.field_of_study
            
            return grade 