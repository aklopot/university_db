# repository_factory.py: Jest to fabryka, która tworzy odpowiednie repozytoria w zależności od konfiguracji. Fabryka ta jest używana w aplikacji do tworzenia repozytoriów, które są używane do interakcji z magazynem danych.
from src.repositories.json_repository import JSONStudentRepository, JSONProfessorRepository
from src.repositories.sqlite_repository import SQLiteStudentRepository, SQLiteProfessorRepository, SQLiteGenderRepository, SQLiteAddressRepository
from src.repositories.postgres_repository import PostgresStudentRepository, PostgresProfessorRepository
from src.repositories.base_student_repository import BaseStudentRepository
from src.repositories.base_professor_repository import BaseProfessorRepository
from src.repositories.base_gender_repository import BaseGenderRepository
from src.repositories.base_address_repository import BaseAddressRepository
from src.config.config_loader import load_config

class RepositoryFactory:
    def __init__(self):
        self.config = load_config()

    def get_student_repository(self) -> BaseStudentRepository:
        data_source = self.config["data_source"]
        
        if data_source == "json":
            return JSONStudentRepository(self.config["json_student_path"])
        elif data_source == "sqlite":
            return SQLiteStudentRepository(self.config["sqlite_url"])
        elif data_source == "postgres":
            return PostgresStudentRepository(self.config["postgres_url"])
        else:
            raise ValueError(f"Nieobsługiwane źródło danych: {data_source}")

    def get_professor_repository(self) -> BaseProfessorRepository:
        data_source = self.config["data_source"]
        
        if data_source == "json":
            return JSONProfessorRepository(self.config["json_professor_path"])
        elif data_source == "sqlite":
            return SQLiteProfessorRepository(self.config["sqlite_url"])
        elif data_source == "postgres":
            return PostgresProfessorRepository(self.config["postgres_url"])
        else:
            raise ValueError(f"Nieobsługiwane źródło danych: {data_source}")

    def get_gender_repository(self) -> BaseGenderRepository:
        data_source = self.config["data_source"]
        if data_source == "sqlite":
            return SQLiteGenderRepository(self.config["sqlite_url"])
        else:
            raise ValueError(f"Nieobsługiwane źródło danych dla płci: {data_source}")
        
    def get_address_repository(self) -> BaseAddressRepository:
        data_source = self.config["data_source"]
        if data_source == "sqlite":
            return SQLiteAddressRepository(self.config["sqlite_url"])
        else:
            raise ValueError(f"Nieobsługiwane źródło danych dla adresów: {data_source}")