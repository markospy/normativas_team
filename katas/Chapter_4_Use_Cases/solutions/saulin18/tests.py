from uuid import uuid4
import pytest


from domain.domain import (
    VeterinariesNotAvailablesException,
    Veterinary, Appointment, AppointmentStatus
)
from domain.abstract_veterinaries_repository import AbstractVeterinariesRepository

from service.service import VeterinaryService
from datetime import datetime


class FakeRepository(AbstractVeterinariesRepository):
    def __init__(self, veterinaries: list[Veterinary]):
        self.veterinaries = veterinaries

    def list(self) -> list[Veterinary]:
        return self.veterinaries

    def get(self, name: str) -> Veterinary:
        for veterinary in self.veterinaries:
            if veterinary.name == name:
                return veterinary
        return None

    def add(self, veterinary: Veterinary) -> None:
        self.veterinaries.append(veterinary)


@pytest.fixture
def fake_repository():
    return FakeRepository(
        [
            Veterinary(
                id=uuid4(),
                name="Dr. López",
                specialty="Felinos",
                appointments=[
                    Appointment(
                        id=uuid4(),
                        date=datetime.now(),
                        specie="Felinos",
                        status=AppointmentStatus.ASSIGNED,
                    )
                ],
            ),
            Veterinary(
                id=uuid4(),
                name="Dr. Ramírez",
                specialty="Perros",
                appointments=[
                    Appointment(
                        id=uuid4(),
                        date=datetime.now(),
                        specie="Perros",
                        status=AppointmentStatus.ASSIGNED,
                    )
                ],
            ),
            Veterinary(
                id=uuid4(),
                name="Dr. Gómez",
                specialty="Aves",
                appointments=[
                    Appointment(
                        id=uuid4(),
                        date=datetime.now(),
                        specie="Aves",
                        status=AppointmentStatus.ASSIGNED,
                    )
                ],
            ),
        ]
    )

@pytest.fixture
def fake_repository_with_veterinary_with_more_than_3_appointments():
    return FakeRepository(
        [
            Veterinary(
                id=uuid4(),
                name="Dr. López",
                specialty="Felinos",
                appointments=[
                    Appointment(
                        id=uuid4(),
                        date=datetime.now(),
                        specie="Felinos",
                        status=AppointmentStatus.ASSIGNED,
                    )
                    for _ in range(3)   
                ],
            ),
        ]
    )


def test_assign_appointment(fake_repository):
    veterinary_service = VeterinaryService(fake_repository)
    appointment = Appointment(
        id=uuid4(),
        date=datetime.now(),
        specie="Felinos",
        status=AppointmentStatus.PENDING,
    )
    veterinary_service.assign_appointment(appointment)
    assert appointment.status == AppointmentStatus.ASSIGNED
    
    
def test_assign_appointment_to_veterinary_not_available_raises_exception(fake_repository):
    veterinary_service = VeterinaryService(fake_repository)
    appointment = Appointment(
        id=uuid4(),
        date=datetime.now(),
        specie="Orangutanes",
        status=AppointmentStatus.PENDING,
    )
    # Raise the error because the specie of the appointment is not handled by any veterinary
    with pytest.raises(VeterinariesNotAvailablesException):
        veterinary_service.assign_appointment(appointment)
        
def test_assign_appointment_to_veterinary_not_available_raises_exception_if_veterinary_has_more_than_3_appointments(fake_repository_with_veterinary_with_more_than_3_appointments):
    veterinary_service = VeterinaryService(fake_repository_with_veterinary_with_more_than_3_appointments)
    appointment = Appointment(
        id=uuid4(),
        date=datetime.now(),
        specie="Felinos",
        status=AppointmentStatus.PENDING,
    )
    with pytest.raises(VeterinariesNotAvailablesException):
        veterinary_service.assign_appointment(appointment)
        
        