from domain import Appointment
from abstract_repository import AbstractRepository
from uuid import UUID

class VeterinaryService:
    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    def assign_appointment(self, appointment_id: UUID, veterinary_id: UUID) -> Appointment:
        appointment = self.repository.get_appointment(appointment_id)
        veterinary = self.repository.get_veterinary(veterinary_id)
        appointment.assign(veterinary)
        return appointment