from typing import List, Optional
from sqlmodel import SQLModel, Session, select, create_engine
from src.models.universitydb import AcademicCourse
from src.repositories.base_repositories.base_academic_course_repository import BaseAcademicCourseRepository
from sqlalchemy.orm import joinedload

class SQLiteAcademicCourseRepository(BaseAcademicCourseRepository):
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.create_all_tables()

    def create_all_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def add_academic_course(self, academic_course: AcademicCourse) -> None:
        with Session(self.engine) as session:
            session.add(academic_course)
            session.commit()

    def update_academic_course(self, academic_course: AcademicCourse) -> None:
        with Session(self.engine) as session:
            existing_course = session.get(AcademicCourse, academic_course.academic_course_id)
            if existing_course:
                existing_course.academic_course_name = academic_course.academic_course_name
                existing_course.ects_credits = academic_course.ects_credits
                existing_course.field_of_study_id = academic_course.field_of_study_id
                session.commit()

    def get_all_academic_courses(self) -> List[AcademicCourse]:
        with Session(self.engine) as session:
            statement = select(AcademicCourse).options(
                joinedload(AcademicCourse.field_of_study)
            )
            return session.exec(statement).all()

    def get_academic_course_by_name(self, name: str) -> Optional[AcademicCourse]:
        with Session(self.engine) as session:
            statement = select(AcademicCourse).where(AcademicCourse.academic_course_name == name)
            return session.exec(statement).first()

    def delete_academic_course_by_id(self, academic_course_id: int) -> None:
        with Session(self.engine) as session:
            academic_course = session.get(AcademicCourse, academic_course_id)
            if academic_course:
                session.delete(academic_course)
                session.commit() 