
import datetime
from uuid import UUID
from enum import Enum

class AppointmentStatus(Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    ATTENDED = "attended"
    
        
class VeterinariesNotAvailablesException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)    

    
class Appointment():
    def __init__(self, id: UUID, date: datetime, specie: str, status: AppointmentStatus):
        self.id = id
        self.date = date
        self.specie = specie
        self.status = status

class Veterinary():    
    def __init__(self, id: UUID, name: str, specialty: str, appointments: list[Appointment]): 
        self.id = id
        self.name = name
        self.specialty = specialty
       
        self.appointments = appointments
    
    def can_accept(self, appointment: Appointment) -> bool:
        # If the veterinary has the same specialty as the appointment and the number of active appointments (ASSIGNED) is less than 3 
        # then the veterinary can accept the appointment
        return self.specialty == appointment.specie and self.verify_active_appointments()
    
    def verify_active_appointments(self) -> bool:
        return len([appointment for appointment in self.appointments if appointment.status == AppointmentStatus.ASSIGNED]) < 3
    
    def assign(self, appointment: Appointment):
        if not self.can_accept(appointment):
            raise VeterinariesNotAvailablesException("Veterinary not available to assign the appointment")
        self.appointments.append(appointment)
        appointment.status = AppointmentStatus.ASSIGNED
    

        

        

           