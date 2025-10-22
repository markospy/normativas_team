import pytest  # noqa: F401

from .exceptions import NoAvailableVet
from .models import AppointmentRequest, Veterinarian, allocate_appointment


@pytest.fixture
def vet():
    return Veterinarian("Dra. López", "canina", max_daily_appointments=3)


@pytest.fixture
def appointments_canina():
    return [
        AppointmentRequest("Marcos", "Roco", "canina", "2025-10-18"),
        AppointmentRequest("Juan", "Firulais", "canina", "2025-10-18"),
        AppointmentRequest("Pedro", "Sansón", "canina", "2025-10-18"),
        AppointmentRequest("María", "Leal", "canina", "2025-10-18"),
        AppointmentRequest("Ana", "Luna", "canina", "2025-10-18"),
        AppointmentRequest("Luis", "Puma", "canina", "2025-10-18"),
        AppointmentRequest("Carlos", "Thor", "canina", "2025-10-18"),
        AppointmentRequest("Sofía", "Nala", "canina", "2025-10-18"),
        AppointmentRequest("Jorge", "Zeus", "canina", "2025-10-18"),
        AppointmentRequest("Laura", "Milo", "canina", "2025-10-18"),
        AppointmentRequest("Diego", "Toby", "canina", "2025-10-18"),
        AppointmentRequest("Valeria", "Kira", "canina", "2025-10-18"),
        AppointmentRequest("Andrés", "Rocky", "canina", "2025-10-18"),
        AppointmentRequest("Lucía", "Mía", "canina", "2025-10-18"),
        AppointmentRequest("Pablo", "Simba", "canina", "2025-10-18"),
        AppointmentRequest("Elena", "Bella", "canina", "2025-10-18"),
        AppointmentRequest("Ricardo", "Apolo", "canina", "2025-10-18"),
        AppointmentRequest("Gabriela", "Lola", "canina", "2025-10-18"),
    ]


@pytest.fixture
def appointments_felina():
    return [
        AppointmentRequest("Carlos", "Toby", "felina", "2025-10-18"),
        AppointmentRequest("José", "Max", "felina", "2025-10-18"),
        AppointmentRequest("Jorge", "Bola", "felina", "2025-10-18"),
        AppointmentRequest("Juan", "Plutón", "felina", "2025-10-18"),
        AppointmentRequest("Marta", "Luna", "felina", "2025-10-18"),
        AppointmentRequest("Claudia", "Misu", "felina", "2025-10-18"),
        AppointmentRequest("Roberto", "Pelusa", "felina", "2025-10-18"),
        AppointmentRequest("Natalia", "Michi", "felina", "2025-10-18"),
        AppointmentRequest("Fernando", "Bigotes", "felina", "2025-10-18"),
        AppointmentRequest("Alejandra", "Mimí", "felina", "2025-10-18"),
    ]


@pytest.fixture
def vets():
    vets = [
        Veterinarian("Dra. López", "canina", max_daily_appointments=7),
        Veterinarian("Dra. Ramírez", "felina", max_daily_appointments=8),
    ]
    return vets


def test_assigning_to_a_vet_reduces_available_slots(vet, appointments_canina):
    vet.assign_appointment(appointments_canina[0])

    assert len(vet._appointments) == 1


def test_assigning_appointment_to_vet_with_less_work_carga(appointments_canina, vets):

    vets[0].assign_appointment(appointments_canina[0])
    vets[0].assign_appointment(appointments_canina[1])
    vets[0].assign_appointment(appointments_canina[2])
    vets[0].assign_appointment(appointments_canina[3])
    vets[0].assign_appointment(appointments_canina[4])
    vets[0].assign_appointment(appointments_canina[5])
    vets[1].assign_appointment(appointments_canina[6])
    vets[1].assign_appointment(appointments_canina[7])
    vets[1].assign_appointment(appointments_canina[8])

    assert allocate_appointment(appointments_canina[9], vets) == vets[0].id


def test_raises_no_available_vet_when_all_vets_are_full(appointments_canina, vets):
    # Llenar completamente ambos veterinarios
    for i in range(7):  # Dra. López tiene max_daily_appointments=7
        vets[0].assign_appointment(appointments_canina[i])

    for i in range(7, 15):  # Dra. Ramírez tiene max_daily_appointments=8
        vets[1].assign_appointment(appointments_canina[i])

    # Intentar asignar una cita adicional cuando ambos están llenos
    with pytest.raises(NoAvailableVet):
        allocate_appointment(appointments_canina[15], vets)


def test_raises_no_available_vet_when_no_vet_matches_specialty(vets):
    exotic_appointment = AppointmentRequest("Juan", "Rex", "exótica", "2025-10-18")

    with pytest.raises(NoAvailableVet):
        allocate_appointment(exotic_appointment, vets)
