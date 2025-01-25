from typing import List, Optional
from src.models.universitydb import AcademicCourse, FieldOfStudy, AcademicStaff
from src.repositories.base_repositories.base_academic_course_repository import BaseAcademicCourseRepository
from src.repositories.base_repositories.base_field_of_study_repository import BaseFieldOfStudyRepository
from src.repositories.base_repositories.base_academic_staff_repository import BaseAcademicStaffRepository
import json

class JSONAcademicCourseRepository(BaseAcademicCourseRepository):
    def __init__(self, file_path: str, 
                 field_of_study_repository: BaseFieldOfStudyRepository,
                 academic_staff_repository: BaseAcademicStaffRepository):
        self.file_path = file_path
        self._field_of_study_repository = field_of_study_repository
        self._academic_staff_repository = academic_staff_repository

    def _create_course_object(self, item: dict) -> AcademicCourse:
        course_data = {
            'academic_course_id': item.get('academic_course_id'),
            'academic_course_name': item.get('academic_course_name'),
            'ects_credits': item.get('ects_credits'),
        }
        
        # Tworzenie obiektu kursu
        course = AcademicCourse(**course_data)
        
        # Dodawanie powiązań
        field_of_study_id = item.get('field_of_study_id')
        if field_of_study_id:
            field_of_study = self._field_of_study_repository.get_field_of_study_by_id(field_of_study_id)
            if field_of_study:
                course.field_of_study = field_of_study
                course.field_of_study_id = field_of_study_id

        academic_staff_id = item.get('academic_staff_id')
        if academic_staff_id:
            academic_staff = self._academic_staff_repository.get_academic_staff_by_id(academic_staff_id)
            if academic_staff:
                course.academic_staff = academic_staff
                course.academic_staff_id = academic_staff_id

        return course

    def _load_data(self) -> List[AcademicCourse]:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [self._create_course_object(item) for item in data.get('courses', [])]
        except FileNotFoundError:
            self._save_data([])
            return []

    def _save_data(self, courses: List[AcademicCourse]) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json_data = {
                'courses': [
                    {
                        'academic_course_id': course.academic_course_id,
                        'academic_course_name': course.academic_course_name,
                        'ects_credits': course.ects_credits,
                        'field_of_study_id': course.field_of_study.field_of_study_id if course.field_of_study else None,
                        'academic_staff_id': course.academic_staff.academic_staff_id if course.academic_staff else None
                    }
                    for course in courses
                ]
            }
            json.dump(json_data, file, indent=4, ensure_ascii=False)

    def add_academic_course(self, course: AcademicCourse) -> None:
        courses = self._load_data()
        # Generowanie nowego ID
        max_id = max([c.academic_course_id or 0 for c in courses], default=0)
        course.academic_course_id = max_id + 1
        courses.append(course)
        self._save_data(courses)

    def get_all_academic_courses(self) -> List[AcademicCourse]:
        return self._load_data()

    def get_academic_course_by_name(self, name: str) -> Optional[AcademicCourse]:
        courses = self._load_data()
        for course in courses:
            if course.academic_course_name.lower() == name.lower():
                return course
        return None

    def update_academic_course(self, course: AcademicCourse) -> None:
        courses = self._load_data()
        for i, c in enumerate(courses):
            if c.academic_course_id == course.academic_course_id:
                # Aktualizujemy wszystkie pola kursu
                courses[i].academic_course_name = course.academic_course_name
                courses[i].ects_credits = course.ects_credits
                courses[i].field_of_study_id = course.field_of_study_id
                courses[i].academic_staff_id = course.academic_staff_id

                # Aktualizujemy obiekty powiązań
                if course.field_of_study:
                    courses[i].field_of_study = self._field_of_study_repository.get_field_of_study_by_id(course.field_of_study_id)
                if course.academic_staff:
                    courses[i].academic_staff = self._academic_staff_repository.get_academic_staff_by_id(course.academic_staff_id)
                break
        self._save_data(courses)

    def delete_academic_course_by_id(self, course_id: int) -> None:
        if course_id is None:
            return
        courses = self._load_data()
        courses = [c for c in courses if c.academic_course_id != course_id]
        self._save_data(courses)

    def add(self, course: AcademicCourse) -> None:
        self.add_academic_course(course)

    def update(self, course: AcademicCourse) -> None:
        self.update_academic_course(course)

    def get_all(self) -> List[AcademicCourse]:
        return self.get_all_academic_courses()

    def delete_by_id(self, course_id: int) -> None:
        self.delete_academic_course_by_id(course_id) 