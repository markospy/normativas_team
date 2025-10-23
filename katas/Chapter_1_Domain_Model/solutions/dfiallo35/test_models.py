
from exceptions import NoAvailableVet
from models import Veterinarian, AppointmentRequest, allocate_appointment


def test_assigning_to_a_vet_reduces_available_slots():
    vet = Veterinarian("Dra. López", "canina", max_daily_appointments=3)
    appointment = AppointmentRequest(
        "Marcos", "Firulais", "canina", "2025-10-18")

    vet.assign(appointment)

    assert len(vet._appointments) == 1


def test_assigning_to_a_vet_not_available_specialty():
    vet = Veterinarian("Dra. López", "canina", max_daily_appointments=3)
    appointment = AppointmentRequest(
        "Marcos", "Firulais", "felina", "2025-10-18")

    response = vet.assign(appointment)
    assert response is False
    assert len(vet._appointments) == 0


def test_assigning_to_a_vet_not_available_slots():
    vet = Veterinarian("Dra. López", "canina", max_daily_appointments=1)
    appointment_1 = AppointmentRequest(
        "Marcos", "Firulais", "canina", "2025-10-18")
    vet.assign(appointment_1)

    appointment_2 = AppointmentRequest(
        "Marcos", "Firulais", "canina", "2025-10-18")

    response = vet.assign(appointment_2)
    assert response is False
    assert len(vet._appointments) == 1


def test_allocate_appoingment_success_1():
    vet_1 = Veterinarian("Dra. López", "canina", max_daily_appointments=3)
    vet_2 = Veterinarian("Dra. Sánchez", "canina", max_daily_appointments=3)

    appointment_1 = AppointmentRequest(
        "Carlos", "Firulais", "canina", "2025-10-18")
    appointment_2 = AppointmentRequest(
        "Bianca", "Firulais", "canina", "2025-10-18")

    vet_1.assign(appointment_1)
    vet_1.assign(appointment_2)

    new_appointment = AppointmentRequest(
        "Carlos", "Firulais", "canina", "2025-10-18")
    allocate_appointment(new_appointment, [vet_1, vet_2])

    assert len(vet_1._appointments) == 2
    assert len(vet_2._appointments) == 1


def test_allocate_appoingment_success_2():
    vet_1 = Veterinarian("Dra. López", "canina", max_daily_appointments=3)
    vet_2 = Veterinarian("Dra. Sánchez", "felina", max_daily_appointments=3)

    appointment_1 = AppointmentRequest(
        "Carlos", "Firulais", "canina", "2025-10-18")
    appointment_2 = AppointmentRequest(
        "Bianca", "Firulais", "canina", "2025-10-18")

    vet_1.assign(appointment_1)
    vet_1.assign(appointment_2)

    new_appointment = AppointmentRequest(
        "Carlos", "Firulais", "canina", "2025-10-18")
    allocate_appointment(new_appointment, [vet_1, vet_2])

    assert len(vet_1._appointments) == 3
    assert len(vet_2._appointments) == 0


def test_allocate_appoingment_fail():
    vet_1 = Veterinarian("Dra. López", "canina", max_daily_appointments=3)

    appointment_1 = AppointmentRequest(
        "Carlos", "Firulais", "felina", "2025-10-18")
    
    try:
        allocate_appointment(appointment_1, [vet_1])
    except Exception as e:
        assert isinstance(e, NoAvailableVet)
        assert str(e) == "No available vet"
