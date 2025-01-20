from typing import List
from sqlmodel import SQLModel, Session, select, create_engine
from src.models.universitydb import AcademicStaff
from src.repositories.base_repositories.base_academic_staff_repository import BaseAcademicStaffRepository
from sqlalchemy.orm import selectinload


class SQLiteAcademicStaffRepository(BaseAcademicStaffRepository):
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.create_all_tables()

    def create_all_tables(self):
        # Upewnij się, że wszystkie wymagane tabele są tworzone w odpowiedniej kolejności
        SQLModel.metadata.create_all(self.engine)

    def add_academic_staff(self, academic_staff: AcademicStaff) -> None:
        with Session(self.engine) as session:
            session.add(academic_staff)
            session.commit()

    def get_all_academic_staff(self) -> List[AcademicStaff]:
        with Session(self.engine) as session:
            statement = select(AcademicStaff).options(
                selectinload(AcademicStaff.gender),
                selectinload(AcademicStaff.address)
            )
            return session.exec(statement).all()

    def delete_academic_staff_by_pesel(self, pesel: str) -> None:
        with Session(self.engine) as session:
            statement = select(AcademicStaff).where(AcademicStaff.pesel == pesel)
            academic_staff = session.exec(statement).first()
            if academic_staff:
                session.delete(academic_staff)
                session.commit()

    def update_academic_staff(self, academic_staff: AcademicStaff) -> None:
        with Session(self.engine) as session:
            existing_academic_staff = session.get(AcademicStaff, academic_staff.academic_staff_id)
            if existing_academic_staff:
                existing_academic_staff.first_name = academic_staff.first_name
                existing_academic_staff.last_name = academic_staff.last_name
                existing_academic_staff.address_id = academic_staff.address_id
                existing_academic_staff.pesel = academic_staff.pesel
                existing_academic_staff.gender_id = academic_staff.gender_id
                existing_academic_staff.position = academic_staff.position
                session.commit()

    def delete_academic_staff_by_id(self, academic_staff_id: int) -> None:
        try:
            with Session(self.engine) as session:
                academic_staff = session.get(AcademicStaff, academic_staff_id)
                if academic_staff:
                    print(f"Znaleziono pracownika do usunięcia: {academic_staff.academic_staff_id}")  # Debug log
                    session.delete(academic_staff)
                    session.commit()
                    print("Pracownik został usunięty")  # Debug log
                else:
                    print(f"Nie znaleziono pracownika o ID: {academic_staff_id}")  # Debug log
        except Exception as e:
            print(f"Błąd w repozytorium podczas usuwania pracownika: {e}")
            raise

    def get_by_last_name(self, last_name: str) -> List[AcademicStaff]:
        with Session(self.engine) as session:
            statement = select(AcademicStaff).where(
                AcademicStaff.last_name.ilike(f"{last_name}%")
            ).options(
                selectinload(AcademicStaff.gender),
                selectinload(AcademicStaff.address)
            )
            return session.exec(statement).all()