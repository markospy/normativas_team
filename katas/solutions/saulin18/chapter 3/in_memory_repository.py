from solution import AppointmentStatus, Appointment, Veterinary
from interfaces import AbstractRepository

from uuid import UUID

class InMemoryRepositoryImpl(AbstractRepository):
    def __init__(self, veterinaries: list[Veterinary]):
        self.veterinaries = {veterinary.id: veterinary for veterinary in veterinaries}
        self.appointments = {}
        
    # Logic for schedule a appointment, same that the last chapter    
    def add(self, appointment: Appointment):
        
        if not appointment.status == AppointmentStatus.PENDING:
            raise ValueError("Appointment is not pending")
        
        for veterinary in sorted(self.veterinaries.values(), key=lambda x: len(x._appointments)):
            if veterinary.can_accept(appointment):
                veterinary.assign(appointment)
                self.appointments[appointment.id] = appointment
                return
        raise ValueError("No veterinarian available to assign the appointment")
    

    def get(self, id: UUID) -> Appointment:
        appointment = self.appointments.get(id)
        if not appointment:
            raise ValueError("Appointment not found")
        return appointment

    def list(self) -> list[Appointment]:
        return list(self.appointments.values())