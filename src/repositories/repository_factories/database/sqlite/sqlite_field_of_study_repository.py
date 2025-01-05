from typing import List, Optional
from sqlmodel import SQLModel, Session, select, create_engine
from src.models.universitydb import FieldOfStudy
from src.repositories.base_repositories.base_field_of_study_repository import BaseFieldOfStudyRepository

class SQLiteFieldOfStudyRepository(BaseFieldOfStudyRepository):
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.create_all_tables()

    def create_all_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def add_field_of_study(self, field_of_study: FieldOfStudy) -> None:
        with Session(self.engine) as session:
            session.add(field_of_study)
            session.commit()

    def update_field_of_study(self, field_of_study: FieldOfStudy) -> None:
        with Session(self.engine) as session:
            existing_field = session.get(FieldOfStudy, field_of_study.field_of_study_id)
            if existing_field:
                existing_field.field_name = field_of_study.field_name
                session.commit()

    def get_all_fields_of_study(self) -> List[FieldOfStudy]:
        with Session(self.engine) as session:
            statement = select(FieldOfStudy)
            return session.exec(statement).all()

    def get_field_of_study_by_name(self, name: str) -> Optional[FieldOfStudy]:
        with Session(self.engine) as session:
            statement = select(FieldOfStudy).where(FieldOfStudy.field_name == name)
            return session.exec(statement).first()

    def delete_field_of_study_by_id(self, field_of_study_id: int) -> None:
        with Session(self.engine) as session:
            field_of_study = session.get(FieldOfStudy, field_of_study_id)
            if field_of_study:
                session.delete(field_of_study)
                session.commit()