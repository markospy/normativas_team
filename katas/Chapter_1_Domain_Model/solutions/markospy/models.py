from uuid import uuid4

from .exceptions import NoAvailableVet


class AppointmentRequest:
    def __init__(self, client_name: str, pet_name: str, specialty: str, date):
        self.id = uuid4()
        self.client_name = client_name
        self.pet_name = pet_name
        self.specialty = specialty
        self.date = date


class Veterinarian:
    def __init__(self, name: str, specialty: str, max_daily_appointments: int):
        self.id = uuid4()
        self.name = name
        self.specialty = specialty
        self.max_daily_appointments = max_daily_appointments
        self._appointments: set[AppointmentRequest] = set()

    def can_accept_appointment(self, appointment_request: AppointmentRequest) -> bool:
        return (
            len(self._appointments) < self.max_daily_appointments and appointment_request.specialty == self.specialty
        )

    def assign_appointment(self, appointment_request: AppointmentRequest):
        if not self.can_accept_appointment(appointment_request):
            return False
        self._appointments.add(appointment_request)
        return True

    def cancel_appointment(self, appointment_request: AppointmentRequest):
        self._appointments.remove(appointment_request)


# Servicio de Dominio: lógica de negocio que reside en el dominio pero que no encaja de forma natural en una entidad o un objeto de valor (como un calculador de impuestos).
def allocate_appointment(appointment: AppointmentRequest, veterinarians: list[Veterinarian]):
    sorted_vets = sorted(
        veterinarians,
        key=lambda vet: (
            vet.max_daily_appointments <= len(vet._appointments),  # False primero (pueden aceptar)
            len(vet._appointments),  # Luego por número de citas
        ),
    )
    for vet in sorted_vets:
        if vet.assign_appointment(appointment):
            return vet.id
    raise NoAvailableVet()
