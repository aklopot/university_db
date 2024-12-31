# postgres_repository.py: Zawiera klasy implementujące interfejsy zdefiniowane w folderze repozytoriów.
# Klasy te korzystają z bazy danych PostgreSQL do przechowywania danych.
from typing import List
from sqlmodel import SQLModel, Session, select, create_engine
from src.models.universitydb import Student, AcademicStaff
from src.repositories.base_repositories.base_student_repository import BaseStudentRepository
from src.repositories.base_repositories.base_academic_staff_repository import BaseAcademicStaffRepository

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

class PostgresAcademicStaffRepository(BaseAcademicStaffRepository):
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        SQLModel.metadata.create_all(self.engine)

    def add_academic_staff(self, academic_staff: AcademicStaff) -> None:
        with Session(self.engine) as session:
            session.add(academic_staff)
            session.commit()

    def get_all_academic_staff(self) -> List[AcademicStaff]:
        with Session(self.engine) as session:
            statement = select(AcademicStaff)
            return session.exec(statement).all()

    def delete_academic_staff_by_pesel(self, pesel: str) -> None:
        with Session(self.engine) as session:
            statement = select(AcademicStaff).where(AcademicStaff.pesel == pesel)
            academic_staff = session.exec(statement).first()
            if academic_staff:
                session.delete(academic_staff)
                session.commit()

    def update_academic_staff(self, academic_staff: AcademicStaff) -> None:
        with Session(self.engine) as session:
            existing_academic_staff = session.get(AcademicStaff, academic_staff.id)
            if existing_academic_staff:
                existing_academic_staff.first_name = academic_staff.first_name
                existing_academic_staff.last_name = academic_staff.last_name
                existing_academic_staff.address = academic_staff.address
                existing_academic_staff.pesel = academic_staff.pesel
                existing_academic_staff.gender = academic_staff.gender
                existing_academic_staff.position = academic_staff.position
                session.commit()
