import pytest
from src.models.universitydb import Student, AcademicCourse, Gender

@pytest.fixture
def sample_student():
    return Student(
        student_id=1,
        index_number="12345",
        first_name="Jan",
        last_name="Kowalski",
        pesel="12345678901",
        gender_id=1,
        field_of_study_id=1
    )

@pytest.fixture
def sample_course():
    return AcademicCourse(
        academic_course_id=1,
        academic_course_name="Matematyka",
        ects_credits=5,
        field_of_study_id=1
    )