# service_factory.py: Zawiera klasę ServiceFactory, która jest odpowiedzialna za dostarczanie instancji klas obsługujących operacje na studentach i pracownikach akademickich.
# Klasa ta przyjmuje konfigurację w konstruktorze i na jej podstawie tworzy instancje StudentService i AcademicStaffService.
from src.services.service_factories.student_service import StudentService
from src.services.service_factories.academic_staff_service import AcademicStaffService
from src.services.service_factories.gender_service import GenderService
from src.services.service_factories.address_service import AddressService
from src.services.service_factories.field_of_study_service import FieldOfStudyService
from src.services.service_factories.academic_course_service import AcademicCourseService
from src.services.service_factories.student_grade_service import StudentGradeService

class ServiceFactory:
    def get_student_service(self) -> StudentService:
        return StudentService()

    def get_academic_staff_service(self) -> AcademicStaffService:
        return AcademicStaffService()
    
    def get_gender_service(self) -> GenderService:
        return GenderService()

    def get_address_service(self) -> AddressService:
        return AddressService()

    def get_field_of_study_service(self) -> FieldOfStudyService:
        return FieldOfStudyService()

    def get_academic_course_service(self) -> AcademicCourseService:
        return AcademicCourseService()

    def get_student_grade_service(self) -> StudentGradeService:
        return StudentGradeService()