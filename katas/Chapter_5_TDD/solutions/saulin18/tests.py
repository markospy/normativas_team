import pytest
from uuid import uuid4
from datetime import datetime
from domain import Appointment, Veterinary, AppointmentStatus
from abstract_repository import AbstractRepository
from service import VeterinaryService
from repository_impl import RepositoryImpl

@pytest.fixture
def repository() -> AbstractRepository:
    return RepositoryImpl()


@pytest.fixture
def service(repository) -> VeterinaryService:
    return VeterinaryService(repository=repository)


@pytest.fixture
def fake_repository() -> AbstractRepository:
    return RepositoryImpl()


def test_assign_appointment(repository, service):
    appointment = Appointment(
        id=uuid4(),
        date=datetime.now(),
        specie="Felinos"
    )
    veterinary = Veterinary(
        id=uuid4(),
        name="Juan Perez",
        specialty="Felino",
    )    
    repository.add_veterinary(veterinary)
    repository.add_appointment(appointment)
    
    result = service.assign_appointment(appointment.id, veterinary.id)
    assert result.id == appointment.id
    assert result.status == AppointmentStatus.ASSIGNED
    
def test_assign_appointment_to_veterinary_not_found(repository, service):
    appointment = Appointment(
        id=uuid4(),
        date=datetime.now(),
        specie="Felinos"
    )
    repository.add_appointment(appointment)
    with pytest.raises(ValueError):
        service.assign_appointment(appointment.id, uuid4())
        
def test_cannot_assign_appointment_to_veterinary_if_appointment_is_not_pending(repository, service):
    appointment = Appointment(
        id=uuid4(),
        date=datetime.now(),
        specie="Felinos",
        status=AppointmentStatus.ASSIGNED
    )
    veterinary = Veterinary(
        id=uuid4(),
        name="Juan Perez",
        specialty="Felino",
    )
    repository.add_veterinary(veterinary)
    repository.add_appointment(appointment)
    with pytest.raises(ValueError):
        service.assign_appointment(appointment.id, veterinary.id)
        
        