from abc import ABC, abstractmethod
from domain.domain import Veterinary

class AbstractVeterinariesRepository(ABC):
    @abstractmethod
    def list(self) -> list[Veterinary]:
        raise NotImplementedError
    
    @abstractmethod
    def get(self, name: str) -> Veterinary:
        raise NotImplementedError
    
    @abstractmethod
    def add(self, veterinary: Veterinary) -> None:
        raise NotImplementedError