# service_factory.py: Zawiera klasę ServiceFactory, która jest odpowiedzialna za dostarczanie instancji klas obsługujących operacje na studentach i profesorach. Klasa ta przyjmuje konfigurację w konstruktorze i na jej podstawie tworzy instancje StudentService i ProfessorService.
from src.services.service_factories.student_service import StudentService
from src.services.service_factories.professor_service import ProfessorService
from src.services.service_factories.gender_service import GenderService
from src.services.service_factories.address_service import AddressService

class ServiceFactory:
    def get_student_service(self) -> StudentService:
        return StudentService()

    def get_professor_service(self) -> ProfessorService:
        return ProfessorService()
    
    def get_gender_service(self) -> GenderService:
        return GenderService()

    def get_address_service(self) -> AddressService:
        return AddressService()