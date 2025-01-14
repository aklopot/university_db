# universitydb.py: Zawiera definicje klas modeli, które reprezentują tabele w bazie danych.
from sqlmodel import SQLModel, Field, Relationship, Column, String, Integer
from typing import Optional, List
from enum import Enum
from sqlalchemy import Enum as SAEnum

class Gender(SQLModel, table=True):
    __tablename__ = "gender"
    gender_id: Optional[int] = Field(default=None, primary_key=True)
    gender_name: str = Field(sa_column=Column(String(100), unique=True, index=True))

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


class FieldOfStudy(SQLModel, table=True):
    __tablename__ = "field_of_study"
    field_of_study_id: Optional[int] = Field(default=None, primary_key=True)
    field_name: str = Field(sa_column=Column(String(100), nullable=False))
    
    students: List["Student"] = Relationship(back_populates="field_of_study")
    academic_course: List["AcademicCourse"] = Relationship(back_populates="field_of_study")

class AcademicCourse(SQLModel, table=True):
    __tablename__ = "academic_course"
    academic_course_id: Optional[int] = Field(default=None, primary_key=True)
    academic_course_name: str = Field(sa_column=Column(String(100), nullable=False))
    ects_credits: int = Field(sa_column=Column(Integer, nullable=False))
    field_of_study_id: Optional[int] = Field(default=None, foreign_key="field_of_study.field_of_study_id")

    field_of_study: Optional[FieldOfStudy] = Relationship(back_populates="academic_course")

class Student(SQLModel, table=True):
    __tablename__ = "student"
    student_id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    address_id: Optional[int] = Field(default=None, foreign_key="address.address_id")
    index_number: str
    pesel: str
    gender_id: Optional[int] = Field(default=None, foreign_key="gender.gender_id")
    field_of_study_id: Optional[int] = Field(default=None, foreign_key="field_of_study.field_of_study_id")
    
    address: Optional[Address] = Relationship(back_populates="students")
    gender: Optional[Gender] = Relationship(back_populates="students")
    field_of_study: Optional[FieldOfStudy] = Relationship(back_populates="students")


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
