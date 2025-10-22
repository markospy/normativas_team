# 🐾 Kata: “Repositorio de pacientes veterinarios”

---

### 🧭 **Contexto**

Este ejercicio nace del **Capítulo 2: Repository Pattern** del libro *Architecture Patterns with Python*.
El objetivo es practicar **cómo separar la lógica de dominio** (entidades y reglas del negocio) de la **infraestructura de datos** (base de datos, ORM, etc.), aplicando el patrón **Repository**.

El contexto es una **clínica veterinaria** que atiende mascotas. Queremos registrar, consultar y mantener actualizada la información de los **pacientes (mascotas)** y su historial de visitas.

---

## 🎯 **Objetivo del ejercicio**

Implementar un pequeño sistema donde:

1. Se defina el **modelo de dominio** (`Pet`, `Visit`).
2. Se cree una **interfaz de repositorio** (`AbstractRepository`).
3. Se implemente una versión en memoria (`FakeRepository`).
4. Se escriban **tests** que usen el repositorio en memoria sin depender de base de datos.

---

## ⚙️ **Instrucciones paso a paso**

### Paso 1️⃣: Modelo de dominio

* Crea una clase `Pet` con los atributos:
  `id`, `name`, `species`, `owner_name`, y una lista de visitas (`visits`).
* Crea una clase `Visit` con los atributos:
  `date`, `reason`, `veterinarian_name`.
* Agrega un método en `Pet` llamado `add_visit()` para registrar una nueva visita.

### Paso 2️⃣: Repositorio abstracto

* Crea una clase abstracta `AbstractRepository` con los métodos:
  `add(pet)`, `get(pet_id)`, y `list()`.

### Paso 3️⃣: Repositorio en memoria

* Implementa `InMemoryPetRepository`, que herede de `AbstractRepository` y almacene los pacientes en una colección Python (como un `dict` o `set`).

### Paso 4️⃣: Tests o uso de ejemplo

* Escribe un test (o función de demostración) que:

  * Cree algunas mascotas.
  * Las agregue al repositorio.
  * Consulte una mascota específica y verifique sus datos.
  * Liste todas las mascotas.

---

## 🧩 **Restricciones**

* Debes aplicar el **Patrón Repository**.
* **No uses librerías externas** (ni bases de datos reales).
* Si haces tests, **usa TDD** o al menos escribe los tests primero.
* El dominio **no debe depender del repositorio ni de infraestructura**.

---

## 🧱 **Nivel**

🔹 **Intermedio** – Ideal para quienes ya manejan clases y POO en Python y desean practicar separación de capas y diseño limpio.

---

## 🧪 **Ejemplo inicial (punto de partida)**

```python
# domain.py
from dataclasses import dataclass
from datetime import date


@dataclass
class Visit:
    date: date
    reason: str
    veterinarian_name: str


class Pet:
    def __init__(self, pet_id: str, name: str, species: str, owner_name: str):
        self.id = pet_id
        self.name = name
        self.species = species
        self.owner_name = owner_name
        self.visits: list[Visit] = []

    def add_visit(self, visit: Visit):
        self.visits.append(visit)
```

```python
# repository.py
import abc
from typing import Optional
from domain import Pet


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, pet: Pet):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, pet_id: str) -> Optional[Pet]:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> list[Pet]:
        raise NotImplementedError
```

```python
# in_memory_repository.py
from repository import AbstractRepository


class InMemoryPetRepository(AbstractRepository):
    def __init__(self):
        self._pets = {}

    def add(self, pet):
        self._pets[pet.id] = pet

    def get(self, pet_id):
        return self._pets.get(pet_id)

    def list(self):
        return list(self._pets.values())
```

```python
# test_repository.py
from datetime import date
from domain import Pet, Visit
from in_memory_repository import InMemoryPetRepository


def test_add_and_get_pet():
    repo = InMemoryPetRepository()
    pet = Pet("P001", "Luna", "Gato", "Marcos")
    pet.add_visit(Visit(date.today(), "Vacunación", "Dra. Paula"))

    repo.add(pet)
    retrieved = repo.get("P001")

    assert retrieved.name == "Luna"
    assert retrieved.visits[0].reason == "Vacunación"
    print("✅ Test passed: Pet added and retrieved successfully!")


if __name__ == "__main__":
    test_add_and_get_pet()
```

---

## 🏁 **Criterio de éxito**

El programador habrá completado el kata correctamente si:

1. Todos los tests pasan.
2. El dominio (`Pet`, `Visit`) no depende del repositorio.
3. El código es claro y sigue una estructura desacoplada.

---

## 🌟 **Versión extendida (opcional)**

Lleva el ejercicio un paso más allá:

1. Implementa un **`SqlAlchemyPetRepository`** que conecte con una base de datos SQLite.
2. Usa un **Unit of Work** para manejar transacciones.
3. Agrega un **servicio de aplicación** que permita registrar nuevas visitas y consulte el historial del paciente.

> Bonus: crea un diagrama que muestre cómo se relacionan `Domain`, `Repository` y `Database`.

---