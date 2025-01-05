from typing import List, Optional
from sqlmodel import SQLModel, Session, select, create_engine
from src.models.universitydb import Gender
from src.repositories.base_repositories.base_gender_repository import BaseGenderRepository

class SQLiteGenderRepository(BaseGenderRepository):
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.create_all_tables()

    def create_all_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def add_gender(self, gender: Gender) -> None:
        with Session(self.engine) as session:
            session.add(gender)
            session.commit()

    def update_gender(self, gender: Gender) -> None:
        with Session(self.engine) as session:
            existing_gender = session.get(Gender, gender.gender_id)
            if existing_gender:
                existing_gender.gender_name = gender.gender_name
                session.commit()

    def get_all_genders(self) -> List[Gender]:
        with Session(self.engine) as session:
            statement = select(Gender)
            return session.exec(statement).all()

    def get_gender_by_name(self, name: str) -> Optional[Gender]:
        with Session(self.engine) as session:
            statement = select(Gender).where(Gender.name == name)
            return session.exec(statement).first()

    def delete_gender_by_id(self, gender_id: int) -> None:
        with Session(self.engine) as session:
            gender = session.get(Gender, gender_id)
            if gender:
                session.delete(gender)
                session.commit()