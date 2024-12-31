# universitydb.py: Zawiera definicje klas modeli, które reprezentują tabele w bazie danych.
from sqlmodel import SQLModel, Field, Relationship, Column, String
from typing import Optional, List
from enum import Enum
from sqlalchemy import Enum as SAEnum

class Gender(SQLModel, table=True):
    __tablename__ = "gender"
    gender_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String, unique=True, index=True))

    students: List["Student"] = Relationship(back_populates="gender")
    academic_staff: List["AcademicStaff"] = Relationship(back_populates="gender")


class Address(SQLModel, table=True):
    __tablename__ = "address"
    address_id: Optional[int] = Field(default=None, primary_key=True)
    street: str
    building_number: str
    city: str
    zip_code: str
    region: str
    country: str

    students: List["Student"] = Relationship(back_populates="address")
    academic_staff: List["AcademicStaff"] = Relationship(back_populates="address")


class Student(SQLModel, table=True):
    __tablename__ = "student"
    student_id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    address_id: Optional[int] = Field(default=None, foreign_key="address.address_id")
    index_number: str
    pesel: str
    gender_id: Optional[int] = Field(default=None, foreign_key="gender.gender_id")
    
    address: Optional[Address] = Relationship(back_populates="students")
    gender: Optional[Gender] = Relationship(back_populates="students")


class AcademicPosition(str, Enum):
    ASSISTANT = "Assistant"
    ASSOCIATE_PROFESSOR = "Associate Professor"
    PROFESSOR = "Professor"
    LECTURER = "Lecturer"

class AcademicStaff(SQLModel, table=True):
    __tablename__ = "academic_staff"
    academic_staff_id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    address_id: Optional[int] = Field(default=None, foreign_key="address.address_id")
    pesel: str
    gender_id: Optional[int] = Field(default=None, foreign_key="gender.gender_id")
    position: AcademicPosition = Field(sa_column=Column(SAEnum(AcademicPosition)))
    
    address: Optional[Address] = Relationship(back_populates="academic_staff")
    gender: Optional[Gender] = Relationship(back_populates="academic_staff")
