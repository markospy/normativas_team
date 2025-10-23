from uuid import uuid4, UUID

from exceptions import NoAvailableVet


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
        self._appointments = set()

    def get_appointments(self):
        return self._appointments.copy()

    def can_accept(self, appointment: AppointmentRequest) -> bool:
        return self.specialty == appointment.specialty and len(self._appointments) < self.max_daily_appointments

    def assign(self, appointment: AppointmentRequest) -> bool:
        if self.can_accept(appointment):
            self._appointments.add(appointment)
            return True
        else:
            return False

    def cancel_appointment(self, appointment_request: AppointmentRequest):
        self._appointments.remove(appointment_request)


def allocate_appointment(vets: list[Veterinarian], appointment: AppointmentRequest) -> UUID:
    vets.sort(key=lambda vet: len(vet.get_appointments()))
    for vet in vets:
        try:
            vet.assign(appointment)
            return vet.id
        except ValueError:
            pass
    raise NoAvailableVet()
