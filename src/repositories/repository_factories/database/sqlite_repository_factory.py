from typing import Dict
from src.repositories.repository_factories.repository_factory_interface import RepositoryFactoryInterface
from src.repositories.repository_factories.database.sqlite.sqlite_student_repository import SQLiteStudentRepository
from src.repositories.repository_factories.database.sqlite.sqlite_academic_staff_repository import SQLiteAcademicStaffRepository
from src.repositories.repository_factories.database.sqlite.sqlite_gender_repository import SQLiteGenderRepository
from src.repositories.repository_factories.database.sqlite.sqlite_address_repository import SQLiteAddressRepository
from src.repositories.repository_factories.database.sqlite.sqlite_field_of_study_repository import SQLiteFieldOfStudyRepository
from src.repositories.repository_factories.database.sqlite.sqlite_academic_course_repository import SQLiteAcademicCourseRepository
from src.repositories.repository_factories.database.sqlite.sqlite_student_grade_repository import SQLiteStudentGradeRepository
from src.repositories.base_repositories.base_student_repository import BaseStudentRepository
from src.repositories.base_repositories.base_academic_staff_repository import BaseAcademicStaffRepository
from src.repositories.base_repositories.base_gender_repository import BaseGenderRepository
from src.repositories.base_repositories.base_address_repository import BaseAddressRepository
from src.repositories.base_repositories.base_field_of_study_repository import BaseFieldOfStudyRepository
from src.repositories.base_repositories.base_academic_course_repository import BaseAcademicCourseRepository
from src.repositories.base_repositories.base_student_grade_repository import BaseStudentGradeRepository

class SQLiteRepositoryFactory(RepositoryFactoryInterface):
    def __init__(self, config: Dict):
        self.config = config
        if 'sqlite_url' not in self.config:
            self.config['sqlite_url'] = "sqlite:///data/sqlite/university.db"  # domyślna ścieżka
        
    def create_student_repository(self) -> BaseStudentRepository:
        return SQLiteStudentRepository(self.config['sqlite_url'])
        
    def create_academic_staff_repository(self) -> BaseAcademicStaffRepository:
        return SQLiteAcademicStaffRepository(self.config['sqlite_url'])
        
    def create_gender_repository(self) -> BaseGenderRepository:
        return SQLiteGenderRepository(self.config["sqlite_url"])
        
    def create_address_repository(self) -> BaseAddressRepository:
        return SQLiteAddressRepository(self.config["sqlite_url"])
        
    def create_field_of_study_repository(self) -> BaseFieldOfStudyRepository:
        return SQLiteFieldOfStudyRepository(self.config["sqlite_url"])
        
    def create_academic_course_repository(self) -> BaseAcademicCourseRepository:
        return SQLiteAcademicCourseRepository(self.config["sqlite_url"])
        
    def create_student_grade_repository(self) -> BaseStudentGradeRepository:
        return SQLiteStudentGradeRepository(self.config["sqlite_url"]) 