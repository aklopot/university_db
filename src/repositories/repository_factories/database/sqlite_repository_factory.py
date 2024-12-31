from src.repositories.repository_factories.repository_factory_interface import RepositoryFactoryInterface
from src.repositories.repository_factories.database.sqlite.sqlite_repository import (
    SQLiteStudentRepository, 
    SQLiteProfessorRepository,
    SQLiteGenderRepository,
    SQLiteAddressRepository
)
from src.repositories.base_repositories.base_student_repository import BaseStudentRepository
from src.repositories.base_repositories.base_professor_repository import BaseProfessorRepository
from src.repositories.base_repositories.base_gender_repository import BaseGenderRepository
from src.repositories.base_repositories.base_address_repository import BaseAddressRepository

class SQLiteRepositoryFactory(RepositoryFactoryInterface):
    def __init__(self, config: dict):
        self.config = config
        
    def create_student_repository(self) -> BaseStudentRepository:
        return SQLiteStudentRepository(self.config["sqlite_url"])
        
    def create_professor_repository(self) -> BaseProfessorRepository:
        return SQLiteProfessorRepository(self.config["sqlite_url"])
        
    def create_gender_repository(self) -> BaseGenderRepository:
        return SQLiteGenderRepository(self.config["sqlite_url"])
        
    def create_address_repository(self) -> BaseAddressRepository:
        return SQLiteAddressRepository(self.config["sqlite_url"]) 