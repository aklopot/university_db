from abc import ABC, abstractmethod
from src.repositories.base_repositories.base_student_repository import BaseStudentRepository
from src.repositories.base_repositories.base_professor_repository import BaseProfessorRepository
from src.repositories.base_repositories.base_gender_repository import BaseGenderRepository
from src.repositories.base_repositories.base_address_repository import BaseAddressRepository

class RepositoryFactoryInterface(ABC):
    """Interfejs fabryki repozytoriów"""
    
    @abstractmethod
    def create_student_repository(self) -> BaseStudentRepository:
        pass
        
    @abstractmethod
    def create_professor_repository(self) -> BaseProfessorRepository:
        pass
        
    @abstractmethod
    def create_gender_repository(self) -> BaseGenderRepository:
        pass
        
    @abstractmethod
    def create_address_repository(self) -> BaseAddressRepository:
        pass 