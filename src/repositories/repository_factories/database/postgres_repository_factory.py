from src.repositories.repository_factories.repository_factory_interface import RepositoryFactoryInterface
from src.repositories.repository_factories.database.postgres.postgres_repository import PostgresStudentRepository, PostgresProfessorRepository
from src.repositories.base_repositories.base_student_repository import BaseStudentRepository
from src.repositories.base_repositories.base_professor_repository import BaseProfessorRepository
from src.repositories.base_repositories.base_gender_repository import BaseGenderRepository
from src.repositories.base_repositories.base_address_repository import BaseAddressRepository

class PostgresRepositoryFactory(RepositoryFactoryInterface):
    def __init__(self, config: dict):
        self.config = config
        
    def create_student_repository(self) -> BaseStudentRepository:
        return PostgresStudentRepository(self.config["postgres_url"])
        
    def create_professor_repository(self) -> BaseProfessorRepository:
        return PostgresProfessorRepository(self.config["postgres_url"])
        
    def create_gender_repository(self) -> BaseGenderRepository:
        raise NotImplementedError("Postgres nie obsługuje repozytoriów płci")
        
    def create_address_repository(self) -> BaseAddressRepository:
        raise NotImplementedError("Postgres nie obsługuje repozytoriów adresów") 