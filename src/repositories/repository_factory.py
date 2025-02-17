# repository_factory.py: Jest to fabryka, która tworzy odpowiednie repozytoria w zależności od konfiguracji
# Fabryka ta jest używana w aplikacji do tworzenia repozytoriów, które są używane do interakcji z danym magazynem danych.
from src.repositories.repository_factories.repository_factory_registry import RepositoryFactoryRegistry
from src.repositories.repository_factories.repository_factory_interface import RepositoryFactoryInterface
from src.repositories.base_repositories.base_student_repository import BaseStudentRepository
from src.repositories.base_repositories.base_academic_staff_repository import BaseAcademicStaffRepository
from src.repositories.base_repositories.base_gender_repository import BaseGenderRepository
from src.repositories.base_repositories.base_address_repository import BaseAddressRepository
from src.repositories.base_repositories.base_field_of_study_repository import BaseFieldOfStudyRepository
from src.repositories.base_repositories.base_academic_course_repository import BaseAcademicCourseRepository
from src.repositories.base_repositories.base_student_grade_repository import BaseStudentGradeRepository
from src.config.config_loader import load_config

class RepositoryFactory:
    def __init__(self):
        self.config = load_config()
        self.factory = self._create_factory()
        
    def _create_factory(self) -> RepositoryFactoryInterface:
        data_source = self.config["data_source"]
        return RepositoryFactoryRegistry.get_factory(data_source, self.config)
    
    def get_student_repository(self) -> BaseStudentRepository:
        return self.factory.create_student_repository()
        
    def get_academic_staff_repository(self) -> BaseAcademicStaffRepository:
        return self.factory.create_academic_staff_repository()
        
    def get_gender_repository(self) -> BaseGenderRepository:
        return self.factory.create_gender_repository()
        
    def get_address_repository(self) -> BaseAddressRepository:
        return self.factory.create_address_repository()
        
    def get_field_of_study_repository(self) -> BaseFieldOfStudyRepository:
        return self.factory.create_field_of_study_repository()
        
    def get_academic_course_repository(self) -> BaseAcademicCourseRepository:
        return self.factory.create_academic_course_repository()

    def get_student_grade_repository(self) -> BaseStudentGradeRepository:
        return self.factory.create_student_grade_repository()