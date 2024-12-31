from src.repositories.repository_factories.repository_factory_interface import RepositoryFactoryInterface
from src.repositories.repository_factories.database.json.json_repository import JSONStudentRepository, JSONProfessorRepository
from src.repositories.base_repositories.base_student_repository import BaseStudentRepository
from src.repositories.base_repositories.base_professor_repository import BaseProfessorRepository
from src.repositories.base_repositories.base_gender_repository import BaseGenderRepository
from src.repositories.base_repositories.base_address_repository import BaseAddressRepository

class JSONRepositoryFactory(RepositoryFactoryInterface):
    def __init__(self, config: dict):
        self.config = config
        
    def create_student_repository(self) -> BaseStudentRepository:
        return JSONStudentRepository(self.config["json_student_path"])
        
    def create_professor_repository(self) -> BaseProfessorRepository:
        return JSONProfessorRepository(self.config["json_professor_path"])
        
    def create_gender_repository(self) -> BaseGenderRepository:
        raise NotImplementedError("JSON nie obsługuje repozytoriów płci")
        
    def create_address_repository(self) -> BaseAddressRepository:
        raise NotImplementedError("JSON nie obsługuje repozytoriów adresów") 