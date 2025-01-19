from typing import List
from sqlmodel import SQLModel, Session, select, create_engine
from src.models.universitydb import StudentGrade, Student
from src.repositories.base_repositories.base_student_grade_repository import BaseStudentGradeRepository
from sqlalchemy.orm import joinedload

class SQLiteStudentGradeRepository(BaseStudentGradeRepository):
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        SQLModel.metadata.create_all(self.engine)

    def add_student_grade(self, grade: StudentGrade) -> None:
        with Session(self.engine) as session:
            session.add(grade)
            session.commit()

    def update_student_grade(self, grade: StudentGrade) -> None:
        with Session(self.engine) as session:
            existing_grade = session.get(StudentGrade, grade.student_grade_id)
            if existing_grade:
                existing_grade.grade_value = grade.grade_value
                existing_grade.grade_type = grade.grade_type
                existing_grade.academic_course_id = grade.academic_course_id
                session.add(existing_grade)
                session.commit()

    def get_student_grades(self, student_id: int) -> List[StudentGrade]:
        with Session(self.engine) as session:
            statement = select(StudentGrade).where(
                StudentGrade.student_id == student_id
            ).options(
                joinedload(StudentGrade.academic_course),
                joinedload(StudentGrade.student)
            )
            return list(session.exec(statement))

    def get_student_grade_by_id(self, grade_id: int) -> StudentGrade:
        with Session(self.engine) as session:
            statement = select(StudentGrade).where(
                StudentGrade.student_grade_id == grade_id
            ).options(
                joinedload(StudentGrade.academic_course),
                joinedload(StudentGrade.student).joinedload(Student.field_of_study)
            )
            return session.exec(statement).first()

    def delete_student_grade_by_id(self, grade_id: int) -> None:
        with Session(self.engine) as session:
            grade = session.get(StudentGrade, grade_id)
            if grade:
                session.delete(grade)
                session.commit() 