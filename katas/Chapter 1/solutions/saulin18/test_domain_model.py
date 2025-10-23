from solution import Veterinarian, AppointmentRequest, allocate_appointment, NoAvailableVet
import pytest

def test_assigning_to_a_vet_reduces_available_slots():
    vet = Veterinarian("Dra. López", "canina", max_daily_appointments=3)
    appointment = AppointmentRequest("Marcos", "Firulais", "canina", "2025-10-18")
    vet.assign(appointment)
    assert len(vet._appointments) == 1
    
def test_cannot_assign_if_specialty_does_not_match():
    vet = Veterinarian("Dra. López", "canina", max_daily_appointments=3)
    appointment = AppointmentRequest("Marcos", "Firulais", "felina", "2025-10-18")
    with pytest.raises(NoAvailableVet):
        vet.assign(appointment)
        
def test_cannot_assign_if_max_daily_appointments_is_reached():
    vet = Veterinarian("Dra. López", "canina", max_daily_appointments=3)
    for _ in range(3):
        appointment = AppointmentRequest("Marcos", "Firulais", "canina", "2025-10-18")
        vet.assign(appointment)
    appointment = AppointmentRequest("Marcos", "Firulais", "canina", "2025-10-18")
    with pytest.raises(NoAvailableVet):
        vet.assign(appointment)
        
def test_allocate_appointment_chooses_the_vet_with_the_least_appointments():
    vet1 = Veterinarian("Dra. López", "canina", max_daily_appointments=3)
    vet2 = Veterinarian("Dra. García", "canina", max_daily_appointments=3)
    vet3 = Veterinarian("Dra. Rodríguez", "canina", max_daily_appointments=3)
    appointment = AppointmentRequest("Marcos", "Firulais", "canina", "2025-10-18")
    allocate_appointment(appointment, [vet1, vet2, vet3])
    assert len(vet1._appointments) == 1
    assert len(vet2._appointments) == 0
    assert len(vet3._appointments) == 0
    
