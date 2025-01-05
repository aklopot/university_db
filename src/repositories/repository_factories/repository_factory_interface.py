from abc import ABC, abstractmethod
from src.repositories.base_repositories.base_student_repository import BaseStudentRepository
from src.repositories.base_repositories.base_academic_staff_repository import BaseAcademicStaffRepository
from src.repositories.base_repositories.base_gender_repository import BaseGenderRepository
from src.repositories.base_repositories.base_address_repository import BaseAddressRepository
from src.repositories.base_repositories.base_field_of_study_repository import BaseFieldOfStudyRepository
from src.repositories.base_repositories.base_academic_course_repository import BaseAcademicCourseRepository

class RepositoryFactoryInterface(ABC):
    """Interfejs fabryki repozytoriów"""
    
    @abstractmethod
    def create_student_repository(self) -> BaseStudentRepository:
        pass
        
    @abstractmethod
    def create_academic_staff_repository(self) -> BaseAcademicStaffRepository:
        pass
        
    @abstractmethod
    def create_gender_repository(self) -> BaseGenderRepository:
        pass
        
    @abstractmethod
    def create_address_repository(self) -> BaseAddressRepository:
        pass
        
    @abstractmethod
    def create_field_of_study_repository(self) -> BaseFieldOfStudyRepository:
        pass
        
    @abstractmethod
    def create_academic_course_repository(self) -> BaseAcademicCourseRepository:
        pass 