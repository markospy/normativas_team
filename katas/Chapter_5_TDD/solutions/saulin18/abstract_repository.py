from abc import ABC, abstractmethod
from domain import Appointment, Veterinary
from uuid import UUID

class AbstractRepository(ABC):
    @abstractmethod
    def get_appointment(self, id: UUID) -> Appointment:
        raise NotImplementedError
    
    
    @abstractmethod
    def get_veterinary(self, id: UUID) -> Veterinary:
        raise NotImplementedError
    
    @abstractmethod
    def add_appointment(self, appointment: Appointment) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def add_veterinary(self, veterinary: Veterinary) -> None:
        raise NotImplementedError
    
    