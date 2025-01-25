from typing import List
from sqlmodel import SQLModel, Session, select, create_engine
from src.models.universitydb import Student
from src.repositories.base_repositories.base_student_repository import BaseStudentRepository
from sqlalchemy.orm import joinedload, selectinload


class SQLiteStudentRepository(BaseStudentRepository):
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.create_all_tables()

    def create_all_tables(self):
        # Upewnij się, że wszystkie wymagane tabele są tworzone w odpowiedniej kolejności
        SQLModel.metadata.create_all(self.engine)

    def add_student(self, student: Student) -> None:
        with Session(self.engine) as session:
            session.add(student)
            session.commit()

    def get_all_students(self) -> List[Student]:
        with Session(self.engine) as session:
            statement = select(Student).options(
                joinedload(Student.gender),
                joinedload(Student.address),
                joinedload(Student.field_of_study)
            )
            return session.exec(statement).all()

    def delete_student_by_index(self, index_number: str) -> None:
        with Session(self.engine) as session:
            statement = select(Student).where(Student.index_number == index_number)
            student = session.exec(statement).first()
            if student:
                session.delete(student)
                session.commit()

    def update_student(self, student: Student) -> None:
        with Session(self.engine) as session:
            existing_student = session.get(Student, student.student_id)
            if existing_student:
                existing_student.first_name = student.first_name
                existing_student.last_name = student.last_name
                existing_student.address_id = student.address_id
                existing_student.index_number = student.index_number
                existing_student.pesel = student.pesel
                existing_student.gender_id = student.gender_id
                existing_student.field_of_study_id = student.field_of_study_id
                session.commit()

    def get_by_last_name(self, last_name: str) -> List[Student]:
        with Session(self.engine) as session:
            statement = select(Student).where(
                Student.last_name.ilike(f"{last_name}%")
            ).options(
                joinedload(Student.gender),
                joinedload(Student.address),
                joinedload(Student.field_of_study)
            )
            return session.exec(statement).all()

    def get_by_pesel(self, pesel: str) -> List[Student]:
        with Session(self.engine) as session:
            statement = select(Student).where(
                Student.pesel.ilike(f"{pesel}%")
            ).options(
                selectinload(Student.gender),
                selectinload(Student.address),
                selectinload(Student.field_of_study)
            )
            return session.exec(statement).all()

    def get_all_students_sorted_by_name(self) -> List[Student]:
        with Session(self.engine) as session:
            statement = select(Student).order_by(Student.last_name, Student.first_name).options(
                joinedload(Student.gender),
                joinedload(Student.address),
                joinedload(Student.field_of_study)
            )
            return session.exec(statement).all()