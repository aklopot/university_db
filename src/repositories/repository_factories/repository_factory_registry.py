from typing import Dict, Type
from src.repositories.repository_factories.repository_factory_interface import RepositoryFactoryInterface

class RepositoryFactoryRegistry:
    """Rejestr fabryk repozytoriów"""
    
    _factories: Dict[str, Type[RepositoryFactoryInterface]] = {}
    
    @classmethod
    def register(cls, data_source: str, factory_class: Type[RepositoryFactoryInterface]) -> None:
        """Rejestruje nową fabrykę dla danego źródła danych"""
        cls._factories[data_source] = factory_class
    
    @classmethod
    def get_factory(cls, data_source: str, config: dict) -> RepositoryFactoryInterface:
        """Zwraca odpowiednią fabrykę dla danego źródła danych"""
        factory_class = cls._factories.get(data_source)
        if not factory_class:
            raise ValueError(f"Nieobsługiwane źródło danych: {data_source}")
        return factory_class(config) 