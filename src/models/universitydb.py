# universitydb.py: Zawiera definicje klas modeli, które reprezentują tabele w bazie danych.
from sqlmodel import SQLModel, Field, Relationship, Column, String, Integer
from typing import Optional, List
from enum import Enum
from sqlalchemy import Enum as SAEnum
from datetime import datetime
from sqlalchemy import Float

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
    academic_staff_id: Optional[int] = Field(default=None, foreign_key="academic_staff.academic_staff_id")

    field_of_study: Optional[FieldOfStudy] = Relationship(back_populates="academic_course")
    academic_staff: Optional["AcademicStaff"] = Relationship(back_populates="academic_courses")
    student_grades: List["StudentGrade"] = Relationship(back_populates="academic_course")

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
    grades: List["StudentGrade"] = Relationship(back_populates="student")


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
    academic_courses: List[AcademicCourse] = Relationship(back_populates="academic_staff")

class GradeType(str, Enum):
    EXAM = "Egzamin"
    FINAL = "Ocena końcowa"
    PROJECT = "Projekt"
    HOMEWORK = "Praca domowa"
    ACTIVITY = "Aktywność"
    MIDTERM = "Kolokwium"
    PRESENTATION = "Prezentacja"
    LABORATORY = "Laboratorium"

class StudentGrade(SQLModel, table=True):
    __tablename__ = "student_grade"
    
    student_grade_id: Optional[int] = Field(default=None, primary_key=True)
    student_id: Optional[int] = Field(default=None, foreign_key="student.student_id")
    academic_course_id: Optional[int] = Field(default=None, foreign_key="academic_course.academic_course_id")
    grade_value: float = Field(sa_column=Column(Float, nullable=False))
    grade_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    grade_type: GradeType = Field(sa_column=Column(SAEnum(GradeType)))
    
    student: Optional["Student"] = Relationship(back_populates="grades")
    academic_course: Optional["AcademicCourse"] = Relationship(back_populates="student_grades")
