from typing import Dict
from src.repositories.repository_factories.repository_factory_interface import RepositoryFactoryInterface
from src.repositories.repository_factories.database.json.json_academic_course_repository import JSONAcademicCourseRepository
from src.repositories.repository_factories.database.json.json_field_of_study_repository import JSONFieldOfStudyRepository
from src.repositories.repository_factories.database.json.json_academic_staff_repository import JSONAcademicStaffRepository
from src.repositories.repository_factories.database.json.json_gender_repository import JSONGenderRepository
from src.repositories.repository_factories.database.json.json_address_repository import JSONAddressRepository
from src.repositories.repository_factories.database.json.json_student_repository import JSONStudentRepository
from src.repositories.repository_factories.database.json.json_student_grade_repository import JSONStudentGradeRepository
from src.repositories.base_repositories.base_academic_course_repository import BaseAcademicCourseRepository
from src.repositories.base_repositories.base_field_of_study_repository import BaseFieldOfStudyRepository
from src.repositories.base_repositories.base_academic_staff_repository import BaseAcademicStaffRepository
from src.repositories.base_repositories.base_student_repository import BaseStudentRepository
from src.repositories.base_repositories.base_student_grade_repository import BaseStudentGradeRepository


class JSONRepositoryFactory(RepositoryFactoryInterface):
    def __init__(self, config: Dict):
        self.config = config["data_source.json"]

    def create_gender_repository(self):
        return JSONGenderRepository(self.config["json_gender_path"])

    def create_address_repository(self):
        return JSONAddressRepository(self.config["json_address_path"])

    def create_field_of_study_repository(self) -> BaseFieldOfStudyRepository:
        return JSONFieldOfStudyRepository(
            self.config["json_field_of_study_path"]
        )

    def create_academic_staff_repository(self) -> BaseAcademicStaffRepository:
        return JSONAcademicStaffRepository(
            self.config["json_academic_staff_path"],
            self.create_gender_repository(),
            self.create_address_repository()
        )

    def create_academic_course_repository(self) -> BaseAcademicCourseRepository:
        return JSONAcademicCourseRepository(
            self.config["json_academic_course_path"],
            self.create_field_of_study_repository(),
            self.create_academic_staff_repository()
        )
    
    def create_student_repository(self) -> BaseStudentRepository:
        return JSONStudentRepository(
            self.config["json_student_path"]
        )

    def create_student_grade_repository(self) -> BaseStudentGradeRepository:
        return JSONStudentGradeRepository(
            self.config["json_student_grade_path"]
        ) 