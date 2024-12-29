# postgres_repository.py: Zawiera klasy implementujące interfejsy zdefiniowane w folderze repozytoriów. Klasy te korzystają z bazy danych PostgreSQL do przechowywania danych.
from typing import List
from sqlmodel import SQLModel, Session, select, create_engine
from src.models.universitydb import Student, Professor
from src.repositories.base_student_repository import BaseStudentRepository
from src.repositories.base_professor_repository import BaseProfessorRepository

class PostgresStudentRepository(BaseStudentRepository):
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        SQLModel.metadata.create_all(self.engine)

    def add_student(self, student: Student) -> None:
        with Session(self.engine) as session:
            session.add(student)
            session.commit()

    def get_all_students(self) -> List[Student]:
        with Session(self.engine) as session:
            statement = select(Student)
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
            existing_student = session.get(Student, student.id)
            if existing_student:
                existing_student.first_name = student.first_name
                existing_student.last_name = student.last_name
                existing_student.address = student.address
                existing_student.index_number = student.index_number
                existing_student.pesel = student.pesel
                existing_student.gender = student.gender
                session.commit()

class PostgresProfessorRepository(BaseProfessorRepository):
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        SQLModel.metadata.create_all(self.engine)

    def add_professor(self, professor: Professor) -> None:
        with Session(self.engine) as session:
            session.add(professor)
            session.commit()

    def get_all_professors(self) -> List[Professor]:
        with Session(self.engine) as session:
            statement = select(Professor)
            return session.exec(statement).all()

    def delete_professor_by_pesel(self, pesel: str) -> None:
        with Session(self.engine) as session:
            statement = select(Professor).where(Professor.pesel == pesel)
            professor = session.exec(statement).first()
            if professor:
                session.delete(professor)
                session.commit()

    def update_professor(self, professor: Professor) -> None:
        with Session(self.engine) as session:
            existing_professor = session.get(Professor, professor.id)
            if existing_professor:
                existing_professor.first_name = professor.first_name
                existing_professor.last_name = professor.last_name
                existing_professor.address = professor.address
                existing_professor.pesel = professor.pesel
                existing_professor.gender = professor.gender
                existing_professor.position = professor.position
                session.commit()
