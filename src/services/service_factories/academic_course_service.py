from typing import List, Optional
from src.models.universitydb import AcademicCourse
from src.repositories.repository_factory import RepositoryFactory

class AcademicCourseService:
    """
    Serwis odpowiedzialny za operacje na kursach akademickich.
    """
    def __init__(self):
        self.repository = RepositoryFactory().get_academic_course_repository()

    def add_academic_course(self, name: str, ects_credits: int, field_of_study_id: int) -> None:
        """
        Dodaje nowy kurs akademicki.
        """
        academic_course = AcademicCourse(
            academic_course_name=name,
            ects_credits=ects_credits,
            field_of_study_id=field_of_study_id
        )
        self.repository.add_academic_course(academic_course)

    def update_academic_course(self, academic_course: AcademicCourse) -> None:
        """
        Aktualizuje dane kursu akademickiego.
        """
        self.repository.update_academic_course(academic_course)

    def get_all_academic_courses(self) -> List[AcademicCourse]:
        """
        Pobiera listę wszystkich kursów akademickich.
        """
        return self.repository.get_all_academic_courses()
    
    def get_academic_course_by_name(self, name: str) -> Optional[AcademicCourse]:
        """
        Pobiera kurs akademicki po nazwie.
        """
        return self.repository.get_academic_course_by_name(name)

    def delete_academic_course(self, academic_course_id: int) -> None:
        """
        Usuwa kurs akademicki o podanym ID.
        """
        self.repository.delete_academic_course_by_id(academic_course_id) 