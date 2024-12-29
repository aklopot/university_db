# sqlite_repository.py: Jest to moduł implementujący interfejsy BaseStudentRepository i BaseProfessorRepository. Używa klas SQLModel i Session z pakietu sqlmodel do interakcji z bazą danych SQLite. Dostarcza metod dodawania, pobierania, usuwania i aktualizowania rekordów studentów i profesorów w bazie danych.
from typing import List, Optional
from sqlmodel import SQLModel, Session, select, create_engine
from src.models.universitydb import Address, Gender, Student, Professor
from src.repositories.base_student_repository import BaseStudentRepository
from src.repositories.base_professor_repository import BaseProfessorRepository
from src.repositories.base_gender_repository import BaseGenderRepository
from src.repositories.base_address_repository import BaseAddressRepository
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
                joinedload(Student.address)
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
            existing_student = session.get(Student, student.address_id)
            if existing_student:
                existing_student.first_name = student.first_name
                existing_student.last_name = student.last_name
                existing_student.address_id = student.address_id
                existing_student.index_number = student.index_number
                existing_student.pesel = student.pesel
                existing_student.gender_id = student.gender_id
                session.commit()

class SQLiteProfessorRepository(BaseProfessorRepository):
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.create_all_tables()

    def create_all_tables(self):
        # Upewnij się, że wszystkie wymagane tabele są tworzone w odpowiedniej kolejności
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
            existing_professor = session.get(Professor, professor.professor_id)
            if existing_professor:
                existing_professor.first_name = professor.first_name
                existing_professor.last_name = professor.last_name
                existing_professor.address_id = professor.address_id
                existing_professor.pesel = professor.pesel
                existing_professor.gender_id = professor.gender_id
                existing_professor.position = professor.position
                session.commit()

    def get_all_professors(self) -> List[Professor]:
        with Session(self.engine) as session:
            statement = select(Professor).options(
                selectinload(Professor.gender),
                selectinload(Professor.address)
            )
            return session.exec(statement).all()

class SQLiteGenderRepository(BaseGenderRepository):
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.create_all_tables()

    def create_all_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def add_gender(self, gender: Gender) -> None:
        with Session(self.engine) as session:
            session.add(gender)
            session.commit()

    def update_gender(self, gender: Gender) -> None:
        with Session(self.engine) as session:
            existing_gender = session.get(Gender, gender.gender_id)
            if existing_gender:
                existing_gender.name = gender.name
                session.commit()

    def get_all_genders(self) -> List[Gender]:
        with Session(self.engine) as session:
            statement = select(Gender)
            return session.exec(statement).all()

    def get_gender_by_name(self, name: str) -> Optional[Gender]:
        with Session(self.engine) as session:
            statement = select(Gender).where(Gender.name == name)
            return session.exec(statement).first()

    def delete_gender_by_id(self, gender_id: int) -> None:
        with Session(self.engine) as session:
            gender = session.get(Gender, gender_id)
            if gender:
                session.delete(gender)
                session.commit()

class SQLiteAddressRepository(BaseAddressRepository):
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.create_all_tables()
    
    def create_all_tables(self):
        SQLModel.metadata.create_all(self.engine)
    
    def add_address(self, address: Address) -> None:
        with Session(self.engine) as session:
            session.add(address)
            session.commit()
    
    def update_address(self, address: Address) -> None:
        with Session(self.engine) as session:
            existing_address = session.get(Address, address.address_id)
            if existing_address:
                existing_address.street = address.street
                existing_address.building_number = address.building_number
                existing_address.city = address.city
                existing_address.zip_code = address.zip_code
                existing_address.region = address.region
                existing_address.country = address.country
                session.commit()
    
    def get_address_by_id(self, address_id: int) -> Optional[Address]:
        with Session(self.engine) as session:
            return session.get(Address, address_id)
        
    def get_all_addresses(self) -> List[Address]:
        with Session(self.engine) as session:
            statement = select(Address)
            return session.exec(statement).all()
    
    def delete_address_by_id(self, address_id: int) -> None:
        with Session(self.engine) as session:
            address = session.get(Address, address_id)
            if address:
                session.delete(address)
                session.commit()