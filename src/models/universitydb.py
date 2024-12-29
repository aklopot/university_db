# universitydb.py: Zawiera definicje klas modeli, które reprezentują tabele w bazie danych.
from sqlmodel import SQLModel, Field, Relationship, Column, String
from typing import Optional, List
from enum import Enum
from sqlalchemy import Enum as SAEnum

class Gender(SQLModel, table=True):
    __tablename__ = "genders"
    gender_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String, unique=True, index=True))

    students: List["Student"] = Relationship(back_populates="gender")
    professors: List["Professor"] = Relationship(back_populates="gender")


class Address(SQLModel, table=True):
    __tablename__ = "addresses"
    address_id: Optional[int] = Field(default=None, primary_key=True)
    street: str
    building_number: str
    city: str
    zip_code: str
    region: str
    country: str

    students: List["Student"] = Relationship(back_populates="address")
    professors: List["Professor"] = Relationship(back_populates="address")


class Student(SQLModel, table=True):
    __tablename__ = "students"
    student_id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    address_id: Optional[int] = Field(default=None, foreign_key="addresses.address_id")
    index_number: str
    pesel: str
    gender_id: Optional[int] = Field(default=None, foreign_key="genders.gender_id")
    
    address: Optional[Address] = Relationship(back_populates="students")
    gender: Optional[Gender] = Relationship(back_populates="students")


class AcademicPosition(str, Enum):
    ASSISTANT = "Assistant"
    ASSOCIATE_PROFESSOR = "Associate Professor"
    PROFESSOR = "Professor"
    LECTURER = "Lecturer"

class Professor(SQLModel, table=True):
    __tablename__ = "professors"
    professor_id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    address_id: Optional[int] = Field(default=None, foreign_key="addresses.address_id")
    pesel: str
    gender_id: Optional[int] = Field(default=None, foreign_key="genders.gender_id")
    position: AcademicPosition = Field(sa_column=Column(SAEnum(AcademicPosition)))
    
    address: Optional[Address] = Relationship(back_populates="professors")
    gender: Optional[Gender] = Relationship(back_populates="professors")
