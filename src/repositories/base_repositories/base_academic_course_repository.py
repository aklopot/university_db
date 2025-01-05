from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.universitydb import AcademicCourse

class BaseAcademicCourseRepository(ABC):
    @abstractmethod
    def add_academic_course(self, academic_course: AcademicCourse) -> None:
        pass

    @abstractmethod
    def update_academic_course(self, academic_course: AcademicCourse) -> None:
        pass
    
    @abstractmethod
    def get_all_academic_courses(self) -> List[AcademicCourse]:
        pass

    @abstractmethod
    def get_academic_course_by_name(self, name: str) -> Optional[AcademicCourse]:
        pass

    @abstractmethod
    def delete_academic_course_by_id(self, academic_course_id: int) -> None:
        pass 