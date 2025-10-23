from uuid import UUID
from solution import Pet
from abc import ABC, abstractmethod


class AbstractPetRepository(ABC):
    @abstractmethod
    def add(self, pet: Pet) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def get(self, id: UUID) -> Pet:
        raise NotImplementedError
    
    @abstractmethod
    def list(self) -> list[Pet]:
        raise NotImplementedError

