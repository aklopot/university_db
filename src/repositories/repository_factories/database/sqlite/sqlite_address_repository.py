from typing import List, Optional
from sqlmodel import SQLModel, Session, select, create_engine
from src.models.universitydb import Address
from src.repositories.base_repositories.base_address_repository import BaseAddressRepository

class SQLiteAddressRepository(BaseAddressRepository):
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.create_all_tables()
    
    def create_all_tables(self):
        SQLModel.metadata.create_all(self.engine)
    
    def add_address(self, address: Address) -> None:
        with Session(self.engine) as session:
            session.add(address)
            session.commit()
    
    def update_address(self, address: Address) -> None:
        with Session(self.engine) as session:
            existing_address = session.get(Address, address.address_id)
            if existing_address:
                existing_address.street = address.street
                existing_address.building_number = address.building_number
                existing_address.city = address.city
                existing_address.zip_code = address.zip_code
                existing_address.region = address.region
                existing_address.country = address.country
                session.commit()
    
    def get_address_by_id(self, address_id: int) -> Optional[Address]:
        with Session(self.engine) as session:
            return session.get(Address, address_id)
        
    def get_all_addresses(self) -> List[Address]:
        with Session(self.engine) as session:
            statement = select(Address)
            return session.exec(statement).all()
    
    def delete_address_by_id(self, address_id: int) -> None:
        with Session(self.engine) as session:
            address = session.get(Address, address_id)
            if address:
                session.delete(address)
                session.commit()