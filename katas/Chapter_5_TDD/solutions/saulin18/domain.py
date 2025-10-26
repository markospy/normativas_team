from uuid import UUID
from datetime import datetime
from enum import Enum
from typing import Optional

class AppointmentStatus(Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    ATTENDED = "attended"
    
class Veterinary():
    def __init__(self, id: UUID, name: str, specialty: str):
        self.id = id
        self.name = name
        self.specialty = specialty
        
        
class Appointment():
    def __init__(self, id: UUID, date: datetime, specie: str, status: Optional[AppointmentStatus] = None):
        self.id = id
        self.date = date
        self.specie = specie
        self.status = status if status else AppointmentStatus.PENDING
        self.veterinary = None
    def assign(self, veterinary: Veterinary):
        if self.status != AppointmentStatus.PENDING:
            raise ValueError("Appointment is not pending")
        self.status = AppointmentStatus.ASSIGNED
        self.veterinary = veterinary
        