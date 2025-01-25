from src.repositories.repository_factories.repository_factory_interface import RepositoryFactoryInterface
from src.repositories.repository_factories.database.json.json_repository import (
    JSONStudentRepository,
    JSONAcademicStaffRepository
)
from src.repositories.repository_factories.database.json.json_field_of_study_repository import JSONFieldOfStudyRepository
from src.repositories.repository_factories.database.json.json_gender_repository import JSONGenderRepository
from src.repositories.base_repositories.base_student_repository import BaseStudentRepository
from src.repositories.base_repositories.base_academic_staff_repository import BaseAcademicStaffRepository
from src.repositories.base_repositories.base_gender_repository import BaseGenderRepository
from src.repositories.base_repositories.base_address_repository import BaseAddressRepository
from src.repositories.base_repositories.base_field_of_study_repository import BaseFieldOfStudyRepository
from src.repositories.base_repositories.base_academic_course_repository import BaseAcademicCourseRepository
from src.repositories.base_repositories.base_student_grade_repository import BaseStudentGradeRepository
from src.repositories.repository_factories.database.json.json_address_repository import JSONAddressRepository
from src.repositories.repository_factories.database.json.json_academic_course_repository import JSONAcademicCourseRepository
from src.repositories.repository_factories.database.json.json_student_grade_repository import JSONStudentGradeRepository

class JSONRepositoryFactory(RepositoryFactoryInterface):
    def __init__(self, config: dict):
        print("DEBUG: Received config:", config)
        self.config = config.get('data_source.json', {})
        self._gender_repository = None
        self._address_repository = None
        
    def create_student_repository(self) -> BaseStudentRepository:
        if 'json_student_path' not in self.config:
            raise ValueError("Missing json_student_path in configuration")
        return JSONStudentRepository(self.config["json_student_path"])
        
    def create_academic_staff_repository(self) -> BaseAcademicStaffRepository:
        if 'json_academic_staff_path' not in self.config:
            raise ValueError("Missing json_academic_staff_path in configuration")
        
        return JSONAcademicStaffRepository(
            self.config['json_academic_staff_path'],
            self._get_gender_repository(),
            self._get_address_repository()
        )
        
    def create_gender_repository(self) -> BaseGenderRepository:
        if 'json_gender_path' not in self.config:
            raise ValueError("Missing json_gender_path in configuration")
        return JSONGenderRepository(self.config["json_gender_path"])

    def create_address_repository(self) -> BaseAddressRepository:
        if 'json_address_path' not in self.config:
            raise ValueError("Missing json_address_path in configuration")
        return JSONAddressRepository(self.config["json_address_path"])

    def _get_gender_repository(self) -> JSONGenderRepository:
        if self._gender_repository is None:
            self._gender_repository = self.create_gender_repository()
        return self._gender_repository

    def _get_address_repository(self) -> JSONAddressRepository:
        if self._address_repository is None:
            self._address_repository = self.create_address_repository()
        return self._address_repository

    def create_field_of_study_repository(self) -> BaseFieldOfStudyRepository:
        if 'json_field_of_study_path' not in self.config:
            raise ValueError("Missing json_field_of_study_path in configuration")
        return JSONFieldOfStudyRepository(self.config["json_field_of_study_path"])

    def create_academic_course_repository(self) -> BaseAcademicCourseRepository:
        if 'json_academic_course_path' not in self.config:
            raise ValueError("Missing json_academic_course_path in configuration")
        return JSONAcademicCourseRepository(self.config["json_academic_course_path"])

    def create_student_grade_repository(self) -> BaseStudentGradeRepository:
        if 'json_student_grade_path' not in self.config:
            raise ValueError("Missing json_student_grade_path in configuration")
        return JSONStudentGradeRepository(self.config['json_student_grade_path']) 