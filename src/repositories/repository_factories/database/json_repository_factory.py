from src.repositories.repository_factories.repository_factory_interface import RepositoryFactoryInterface
from src.repositories.repository_factories.database.json.json_repository import JSONStudentRepository, JSONAcademicStaffRepository
from src.repositories.base_repositories.base_student_repository import BaseStudentRepository
from src.repositories.base_repositories.base_academic_staff_repository import BaseAcademicStaffRepository
from src.repositories.base_repositories.base_gender_repository import BaseGenderRepository
from src.repositories.base_repositories.base_address_repository import BaseAddressRepository

class JSONRepositoryFactory(RepositoryFactoryInterface):
    def __init__(self, config: dict):
        self.config = config
        
    def create_student_repository(self) -> BaseStudentRepository:
        return JSONStudentRepository(self.config["json_student_path"])
        
    def create_academic_staff_repository(self) -> BaseAcademicStaffRepository:
        return JSONAcademicStaffRepository(self.config["json_academic_staff_path"])
        
    def create_gender_repository(self) -> BaseGenderRepository:
        raise NotImplementedError("JSON nie obsługuje repozytoriów płci")
        
    def create_address_repository(self) -> BaseAddressRepository:
        raise NotImplementedError("JSON nie obsługuje repozytoriów adresów") 