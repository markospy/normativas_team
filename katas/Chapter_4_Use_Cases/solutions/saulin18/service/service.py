from domain.domain import Appointment, VeterinariesNotAvailablesException
from domain.abstract_veterinaries_repository import AbstractVeterinariesRepository

class VeterinaryService:
    def __init__(self, veterinary_repository: AbstractVeterinariesRepository):
        self.veterinary_repository = veterinary_repository
    
    def assign_appointment(self, appointment: Appointment):
        for veterinary in self.veterinary_repository.list():
            if veterinary.can_accept(appointment):
                veterinary.assign(appointment)
                return
        raise VeterinariesNotAvailablesException("No veterinaries available to assign the appointment")