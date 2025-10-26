import datetime
import pytest

from in_memory_repository import InMemoryRepositoryImpl
from service import VeterinaryService
from solution import Pet, Appointment, Veterinary, AppointmentStatus
from uuid import UUID


@pytest.fixture
def repository() -> InMemoryRepositoryImpl:
    return InMemoryRepositoryImpl()


class FakeRepository(InMemoryRepositoryImpl):
    def __init__(self, veterinaries: list[Veterinary]):
        super().__init__(veterinaries)

    def add(self, appointment: Appointment):
        super().add(appointment)

    def get(self, id: UUID) -> Appointment:
        return super().get(id)

    def list(self) -> list[Appointment]:
        return super().list()


@pytest.fixture
def myFakeRepository() -> FakeRepository:
    return FakeRepository(
        [
            Veterinary(
                name="Dr. López", specialty="Felinos", max_daily_appointments=10
            ),
            Veterinary(name="Dr. Ramírez", specialty="Perro", max_daily_appointments=2),
            Veterinary(name="Dr. Gómez", specialty="Aves", max_daily_appointments=5),
        ]
    )


def test_schedule_appointment(myFakeRepository: FakeRepository):
    appointment = Appointment(
        pet=Pet(name="Firulais", specie="Perro", owner="Juan"),
        date=datetime.datetime.now(),
    )
    myFakeRepository.add(appointment)

    assert len(myFakeRepository.list()) == 1


def test_get_all_appointments(myFakeRepository: FakeRepository):
    appointment1 = Appointment(
        pet=Pet(name="Firulais", specie="Perro", owner="Juan"),
        date=datetime.datetime.now(),
    )
    appointment2 = Appointment(
        pet=Pet(name="Mittens", specie="Felinos", owner="Ana"),
        date=datetime.datetime.now(),
    )
    myFakeRepository.add(appointment1)
    myFakeRepository.add(appointment2)
    appointments = myFakeRepository.list()
    assert len(appointments) == 2


def test_get_appointment_by_id(myFakeRepository: FakeRepository):
    appointment = Appointment(
        pet=Pet(name="Firulais", specie="Perro", owner="Juan"),
        date=datetime.datetime.now(),
    )
    myFakeRepository.add(appointment)
    retrieved_appointment = myFakeRepository.get(appointment.id)
    assert retrieved_appointment.id == appointment.id
    assert retrieved_appointment.pet.name == "Firulais"
