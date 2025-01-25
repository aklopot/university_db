# Repozytorium dla pracowników akademickich
from typing import Dict, List, Optional
from src.models.universitydb import AcademicStaff
from src.repositories.base_repositories.base_academic_staff_repository import BaseAcademicStaffRepository
from src.repositories.base_repositories.base_gender_repository import BaseGenderRepository
from src.repositories.base_repositories.base_address_repository import BaseAddressRepository
import json

class JSONAcademicStaffRepository(BaseAcademicStaffRepository):
    def __init__(self, file_path: str, gender_repository: BaseGenderRepository, address_repository: BaseAddressRepository):
        self.file_path = file_path
        self._gender_repository = gender_repository
        self._address_repository = address_repository

    def _create_staff_object(self, data: Dict) -> AcademicStaff:
        # Tworzymy kopię danych
        staff_data = data.copy()
        
        # Pobieramy i usuwamy ID relacji
        gender_id = staff_data.pop('gender_id', None)
        address_id = staff_data.pop('address_id', None)
        
        # Normalizujemy wartość position
        if 'position' in staff_data:
            position_mapping = {
                'PROFESSOR': 'Professor',
                'ASSISTANT': 'Assistant',
                'ASSOCIATE_PROFESSOR': 'Associate Professor',
                'LECTURER': 'Lecturer'
            }
            staff_data['position'] = position_mapping.get(staff_data['position'], staff_data['position'])
        
        # Tworzymy obiekt bez relacji
        staff = AcademicStaff.model_validate(staff_data)
        
        # Dodajemy relacje
        if gender_id is not None:
            gender = self._gender_repository.get_gender_by_id(gender_id)
            if gender:
                staff.gender = gender
                
        if address_id is not None:
            address = self._address_repository.get_address_by_id(address_id)
            if address:
                staff.address = address
                
        return staff

    def _load_data(self) -> List[AcademicStaff]:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [self._create_staff_object(item) for item in data]
        except FileNotFoundError:
            return []

    def _save_data(self, academic_staff_list: List[AcademicStaff]) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json_data = []
            for staff in academic_staff_list:
                staff_dict = staff.model_dump(exclude={'gender', 'address'})
                if staff.gender:
                    staff_dict['gender_id'] = staff.gender.gender_id
                if staff.address:
                    staff_dict['address_id'] = staff.address.address_id
                json_data.append(staff_dict)
            json.dump(json_data, file, indent=4, ensure_ascii=False)

    def add_academic_staff(self, academic_staff: AcademicStaff) -> None:
        academic_staff_list = self._load_data()
        academic_staff_list.append(academic_staff)
        self._save_data(academic_staff_list)

    def get_all_academic_staff(self) -> List[AcademicStaff]:
        return self._load_data()

    def delete_academic_staff_by_pesel(self, pesel: str) -> None:
        academic_staff_list = self._load_data()
        academic_staff_list = [p for p in academic_staff_list if p.pesel != pesel]
        self._save_data(academic_staff_list)

    def update_academic_staff(self, academic_staff: AcademicStaff) -> None:
        academic_staff_list = self._load_data()
        for i, p in enumerate(academic_staff_list):
            if p.pesel == academic_staff.pesel:
                academic_staff_list[i] = academic_staff
                break
        self._save_data(academic_staff_list)

    def get_by_last_name(self, last_name: str) -> List[AcademicStaff]:
        """
        Pobiera wszystkich pracowników o podanym nazwisku.
        
        Args:
            last_name (str): Nazwisko do wyszukania
            
        Returns:
            List[AcademicStaff]: Lista znalezionych pracowników
        """
        staff_list = self._load_data()
        return [staff for staff in staff_list if staff.last_name.lower() == last_name.lower()]

    def get_academic_staff_by_id(self, staff_id: int) -> Optional[AcademicStaff]:
        """
        Pobiera pracownika akademickiego po ID.
        
        Args:
            staff_id (int): ID pracownika
            
        Returns:
            Optional[AcademicStaff]: Znaleziony pracownik lub None
        """
        staff_list = self._load_data()
        for staff in staff_list:
            if staff.academic_staff_id == staff_id:
                return staff
        return None
