from src.repositories.repository_factories.repository_factory_interface import RepositoryFactoryInterface
from src.repositories.repository_factories.database.postgres.postgres_repository import PostgresStudentRepository, PostgresAcademicStaffRepository
from src.repositories.base_repositories.base_student_repository import BaseStudentRepository
from src.repositories.base_repositories.base_academic_staff_repository import BaseAcademicStaffRepository
from src.repositories.base_repositories.base_gender_repository import BaseGenderRepository
from src.repositories.base_repositories.base_address_repository import BaseAddressRepository

class PostgresRepositoryFactory(RepositoryFactoryInterface):
    def __init__(self, config: dict):
        self.config = config
        
    def create_student_repository(self) -> BaseStudentRepository:
        return PostgresStudentRepository(self.config["postgres_url"])
        
    def create_academic_staff_repository(self) -> BaseAcademicStaffRepository:
        return PostgresAcademicStaffRepository(self.config["postgres_url"])
        
    def create_gender_repository(self) -> BaseGenderRepository:
        raise NotImplementedError("Postgres nie obsługuje repozytoriów płci")
        
    def create_address_repository(self) -> BaseAddressRepository:
        raise NotImplementedError("Postgres nie obsługuje repozytoriów adresów") 