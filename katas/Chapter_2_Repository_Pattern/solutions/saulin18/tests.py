
from solution import Pet, Visit
import pytest
from uuid import UUID
from abstract_pet_repository import AbstractPetRepository

class InMemoryPetRepositoryImpl(AbstractPetRepository):
    def __init__(self):
        self.pets = {}
    
    def add(self, pet: Pet) -> None:
        self.pets[pet.id] = pet
    
    def get(self, id: UUID) -> Pet:
        return self.pets.get(id)
    
    def list(self) -> list[Pet]:
        return list(self.pets.values())

@pytest.fixture
def pet_repository() -> AbstractPetRepository:
    return InMemoryPetRepositoryImpl()

def test_add_and_get_pet(pet_repository: AbstractPetRepository):
    pet = Pet(name="Fido", species="Dog", owner_name="John Doe")
    pet_repository.add(pet)
    assert pet_repository.get(pet.id) == pet

def test_list_pets(pet_repository: AbstractPetRepository):
    pet = Pet(name="Fido", species="Dog", owner_name="John Doe")
    pet_repository.add(pet)
    assert pet_repository.list() == [pet]
    
def test_add_visit_to_pet(pet_repository: AbstractPetRepository):
    pet = Pet(name="Fido", species="Dog", owner_name="John Doe")
    visit = Visit(reason="Checkup", veterinarian_name="Dr. Smith")
    pet.add_visit(visit)
    pet_repository.add(pet)
    assert pet.visits == [visit]
    assert pet_repository.get(pet.id).visits == [visit]