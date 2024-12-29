# service_factory.py: Zawiera klasę ServiceFactory, która jest odpowiedzialna za dostarczanie instancji klas obsługujących operacje na studentach i profesorach. Klasa ta przyjmuje konfigurację w konstruktorze i na jej podstawie tworzy instancje StudentService i ProfessorService.
from src.services.student_service import StudentService
from src.services.professor_service import ProfessorService
from src.services.gender_service import GenderService
from src.services.address_service import AddressService

class ServiceFactory:
    def __init__(self, config):
        self.config = config

    def get_student_service(self) -> StudentService:
        return StudentService(self.config)

    def get_professor_service(self) -> ProfessorService:
        return ProfessorService(self.config)
    
    def get_gender_service(self) -> GenderService:
        return GenderService(self.config)

    def get_address_service(self) -> AddressService:
        return AddressService(self.config)