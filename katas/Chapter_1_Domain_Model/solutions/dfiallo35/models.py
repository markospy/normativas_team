import datetime

from exceptions import NoAvailableVet


class BaseEntity:
    def model_dump(self):
        return self.__dict__


class AppointmentRequest(BaseEntity):
    def __init__(self, client_name: str, pet_name: str, specialty: str, date: datetime.date):
        super().__init__()
        self.client_name = client_name
        self.pet_name = pet_name
        self.specialty = specialty
        self.date = date


class Veterinarian(BaseEntity):
    def __init__(self, name: str, specialty: str, max_daily_appointments: int):
        super().__init__()
        self.name = name
        self.specialty = specialty
        self.max_daily_appointments = max_daily_appointments
        self._appointments = set()

    def can_accept(self, appointment: AppointmentRequest) -> bool:
        return appointment.specialty == self.specialty and len(self._appointments) < self.max_daily_appointments

    def assign(self, appointment: AppointmentRequest) -> True:
        if self.can_accept(appointment):
            self._appointments.add(appointment)
            return True

        return False


def allocate_appointment(appointment, veterinarians) -> None:
    for vet in sorted(veterinarians, key=lambda v: len(v._appointments)):
        if vet.assign(appointment):
            return
    return NoAvailableVet("No available vet")
