from abc import ABC, abstractmethod
from typing import Any

class AbstractRepository(ABC):
    @abstractmethod
    def add(self, entity: Any) -> None:
        pass
    
    @abstractmethod
    def get(self, id: Any) -> Any:
        pass
    
    @abstractmethod
    def list(self) -> list[Any]:
        pass