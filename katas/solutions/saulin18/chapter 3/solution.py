import datetime
from typing import Set
from enum import Enum
import uuid
from uuid import UUID


class AppointmentStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"


class Pet:
    id: UUID
    name: str
    specie: str
    owner: str

    def __init__(self, name: str, specie: str, owner: str):
        self.id = uuid.uuid4()
        self.name = name
        self.specie = specie
        self.owner = owner


class Appointment:
    id: UUID
    status: AppointmentStatus
    date: datetime.datetime
    pet: Pet

    def __init__(self, date: datetime.datetime, pet: Pet):
        self.id = uuid.uuid4()
        self.date = date
        self.pet = pet
        self.status = AppointmentStatus.PENDING


class Veterinary:
    def __init__(self, name: str, specialty: str, max_daily_appointments: int):
        self.id = uuid.uuid4()
        self.name = name
        self.specialty = specialty
        self.max_daily_appointments = max_daily_appointments
        self._appointments: Set[Appointment] = set()

    def can_accept(self, appointment: Appointment) -> bool:
        return (
            self.specialty == appointment.pet.specie
            and len(self._appointments) < self.max_daily_appointments
        )

    def assign(self, appointment: Appointment):
        if not self.can_accept(appointment):
            raise ValueError("Veterinary cannot accept the appointment")
        self._appointments.add(appointment)
        appointment.status = AppointmentStatus.CONFIRMED
