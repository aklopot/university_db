import pytest
from unittest.mock import Mock, patch
from src.models.universitydb import StudentGrade, Student, AcademicCourse
from src.services.service_factories.student_grade_service import StudentGradeService
from src.repositories.repository_factory import RepositoryFactory
from datetime import datetime, UTC, timezone

@pytest.fixture
def test_date():
    return datetime(2024, 1, 1, tzinfo=UTC)

@pytest.fixture
def mock_repository():
    repository = Mock()
    repository.get_student_grades.return_value = []
    repository.get_student_grade_by_id.return_value = None
    return repository

@pytest.fixture
def service(mock_repository):
    with patch.object(RepositoryFactory, 'get_student_grade_repository', return_value=mock_repository):
        return StudentGradeService()

@pytest.fixture
def sample_grade(test_date):
    return StudentGrade(
        grade_id=1,
        grade_value=4.5,
        student_id=1,
        academic_course_id=1,
        date=test_date
    )

def test_get_student_grades(service, mock_repository, test_date):
    # Arrange
    student_id = 1
    expected_grades = [
        StudentGrade(
            grade_id=1, 
            grade_value=4.5, 
            student_id=1, 
            academic_course_id=1,
            date=test_date
        ),
        StudentGrade(
            grade_id=2, 
            grade_value=5.0, 
            student_id=1, 
            academic_course_id=2,
            date=test_date
        )
    ]
    mock_repository.get_student_grades.return_value = expected_grades

    # Act
    result = service.get_student_grades(student_id)

    # Assert
    assert result == expected_grades
    mock_repository.get_student_grades.assert_called_once_with(student_id)

def test_add_student_grade(service, mock_repository, sample_grade):
    # Act
    service.add_student_grade(sample_grade)

    # Assert
    mock_repository.add_student_grade.assert_called_once_with(sample_grade)

def test_update_student_grade(service, mock_repository, sample_grade):
    # Act
    service.update_student_grade(sample_grade)

    # Assert
    mock_repository.update_student_grade.assert_called_once_with(sample_grade)

def test_delete_student_grade(service, mock_repository):
    # Arrange
    grade_id = 1

    # Act
    service.delete_student_grade(grade_id)

    # Assert
    mock_repository.delete_student_grade_by_id.assert_called_once_with(grade_id)

def test_get_grade(service, mock_repository, sample_grade):
    # Arrange
    grade_id = 1
    mock_repository.get_student_grade_by_id.return_value = sample_grade

    # Act
    result = service.get_grade(grade_id)

    # Assert
    assert result == sample_grade
    mock_repository.get_student_grade_by_id.assert_called_once_with(grade_id)