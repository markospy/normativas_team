from interfaces import AbstractRepository
from solution import Appointment, Pet


class VeterinaryService():
    def __init__(self, repository: AbstractRepository):
        self.repository = repository
        
    def schedule_appointment(self, pet: Pet):
        appointment = Appointment(pet=pet)
        self.repository.add(appointment)
        
    def get_all_appointments(self):
        return self.repository.list()
        
