from typing import Set, List, Optional

class AppointmentRequest:
    def __init__(self, client_name: str, pet_name: str, specialty: str, date: str):
        self.client_name = client_name
        self.pet_name = pet_name
        self.specialty = specialty
        self.date = date
        
        
class Veterinarian:
    def __init__(self, name: str, specialty: str, max_daily_appointments: int):
        self.name = name
        self.specialty = specialty
        self.max_daily_appointments = max_daily_appointments
        self._appointments: Set[AppointmentRequest] = set()
        
    def can_accept(self, appointment: AppointmentRequest) -> bool:
        return self.specialty == appointment.specialty and len(self._appointments) < self.max_daily_appointments
        
    def assign(self, appointment: AppointmentRequest):
        if not self.can_accept(appointment):
            raise NoAvailableVet(f"No puede asignar la cita porque no tiene la especialidad correcta o ya alcanzó su límite diario de citas")
        self._appointments.add(appointment)
        
def allocate_appointment(appointment: AppointmentRequest, veterinarians: List[Veterinarian]) -> Veterinarian:
    # Order the veterinarians by the number of appointments they have in ascending order
    for vet in sorted(veterinarians, key=lambda x: len(x._appointments)):
        if vet.can_accept(appointment):
            vet.assign(appointment)
            return vet
    raise NoAvailableVet(f"No hay veterinario disponible para asignar la cita ")

class NoAvailableVet(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)