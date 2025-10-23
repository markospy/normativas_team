from domain_model import Veterinarian, AppointmentRequest, allocate_appointment
import pytest
from exceptions import NoAvailableVet


def test_assigning_to_a_vet_reduces_available_slots():
    vet = Veterinarian("Dra. López", "canina", max_daily_appointments=3)
    appointment = AppointmentRequest("Marcos", "Firulais", "canina", "2025-10-18")

    vet.assign(appointment)

    assert len(vet._appointments) == 1

def test_assigning_specialty_mismatch_fails():
    vet = Veterinarian("Dra. López", "canina", max_daily_appointments=3)
    appointment = AppointmentRequest("Marcos", "Firulais", "felina", "2025-10-18")

    with pytest.raises(NoAvailableVet):
        vet.assign(appointment)

def test_assigning_to_a_full_vet_fails():
    vet = Veterinarian("Dra. López", "canina", max_daily_appointments=1)
    appointment1 = AppointmentRequest("Marcos", "Firulais", "canina", "2025-10-18")
    appointment2 = AppointmentRequest("Daniel", "Flopy", "canina", "2025-10-18")

    vet.assign(appointment1)

    with pytest.raises(NoAvailableVet):
        vet.assign(appointment2)

def test_allocate_appointment_chooses_vet_with_fewer_appointments():
    vet1 = Veterinarian("Dra. López", "canina", max_daily_appointments=3)
    vet2 = Veterinarian("Dra. López", "canina", max_daily_appointments=3)
    appointment1 = AppointmentRequest("Marcos", "Firulais", "canina", "2025-10-18")
    appointment2 = AppointmentRequest("Daniel", "Flopy", "canina", "2025-10-18")
    appointment3 = AppointmentRequest("Juan", "Max", "canina", "2025-10-18")

    vet1.assign(appointment1)
    vet1.assign(appointment3)
    vet2.assign(appointment2)

    vets = [vet1, vet2]

    assert allocate_appointment(vets, AppointmentRequest("Juan", "Max", "canina", "2025-10-18")) == vet2.id


