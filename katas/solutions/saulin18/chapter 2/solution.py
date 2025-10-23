
import datetime
from uuid import UUID, uuid4

class Visit():
    id: UUID
    veterinarian_name: str
    date: datetime
    reason: str
    
    def __init__(self, id: UUID = None, date: datetime.date = datetime.date.today(), reason: str = "", veterinarian_name: str = "") -> None:
        self.id = id if id else uuid4()
        self.date = date
        self.reason = reason
        self.veterinarian_name = veterinarian_name
    

class Pet():
    id: UUID
    name: str
    species: str
    owner_name: str
    visits: list[Visit]
    
    def __init__(self, id: UUID = None, name: str = "", species: str = "", owner_name: str = "") -> None:
        self.id = id if id else uuid4()
        self.name = name
        self.species = species
        self.owner_name = owner_name
        self.visits = []
        
    def add_visit(self, visit: Visit) -> None:
        self.visits.append(visit)
        
        
        