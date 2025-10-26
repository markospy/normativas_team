from abstract_repository import AbstractRepository
from domain import Veterinary, Appointment
from uuid import UUID

class RepositoryImpl(AbstractRepository):
    def __init__(self):
        self.veterinaries = {}
        self.appointments = {}
        
    def get_veterinary(self, id: UUID) -> Veterinary:
        veterinary = self.veterinaries.get(id)
        if not veterinary:
            raise ValueError("Veterinary not found")
        return veterinary
            
    def get_appointment(self, id: UUID) -> Appointment:
        appointment = self.appointments.get(id)
        if not appointment:
            raise ValueError("Appointment not found")
        return appointment
        
    def add_veterinary(self, veterinary: Veterinary) -> None:
        self.veterinaries[veterinary.id] = veterinary
        
    def add_appointment(self, appointment: Appointment) -> None:
        self.appointments[appointment.id] = appointment