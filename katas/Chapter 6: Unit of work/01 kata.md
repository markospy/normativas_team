# 🧩 Kata: “Unidad de Trabajo Veterinaria”

### 🧠 Contexto

Este ejercicio surge del patrón **Unit of Work**, estudiado en el capítulo 6 del libro *Architecture Patterns with Python*.
En una arquitectura limpia, el patrón **Unit of Work** coordina los cambios realizados a través de múltiples repositorios dentro de una misma transacción.
En este kata, simularás una operación típica de una clínica veterinaria: **registrar una consulta médica y actualizar el historial del paciente**, garantizando que ambas operaciones se guarden o se deshagan juntas.

---

## 🎯 Objetivo

Implementar una **clase `UnitOfWork`** que:

1. Coordine múltiples repositorios bajo una misma transacción.
2. Permita confirmar (`commit`) o revertir (`rollback`) los cambios.
3. Aísle la lógica de negocio del detalle de persistencia.
4. Pase las pruebas escritas siguiendo el enfoque **TDD (Test Driven Development)**.

---

## 🧩 Dominio del problema

Una clínica veterinaria tiene:

* **Pacientes (Mascotas)** que pertenecen a un dueño.
* **Consultas** que registran una atención médica.

El caso de uso que implementarás es:

> Registrar una nueva consulta.
> Si la operación es exitosa, la consulta y el cambio en el historial del paciente deben guardarse.
> Si ocurre un error, **nada debe persistir**.

---

## ⚙️ Instrucciones paso a paso

### Paso 1: Crear las Entidades del Dominio

Implementa las clases básicas:

```python
# domain/models.py

class Mascota:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.historial = []

    def agregar_consulta(self, consulta):
        self.historial.append(consulta)


class Consulta:
    def __init__(self, id, mascota_id, motivo):
        self.id = id
        self.mascota_id = mascota_id
        self.motivo = motivo
```

---

### Paso 2: Definir la Abstracción del Repositorio

```python
# domain/abstract_repository.py

from abc import ABC, abstractmethod

class AbstractRepository(ABC):
    @abstractmethod
    def add(self, entity):
        pass

    @abstractmethod
    def get(self, id):
        pass
```

Y un repositorio en memoria para pruebas:

```python
# adapters/repository_memory.py

from domain.abstract_repository import AbstractRepository

class InMemoryRepository(AbstractRepository):
    def __init__(self):
        self._data = {}

    def add(self, entity):
        self._data[entity.id] = entity

    def get(self, id):
        return self._data.get(id)
```

---

### Paso 3: Crear la Abstracción del Unit of Work

```python
# service_layer/unit_of_work.py

from abc import ABC, abstractmethod

class AbstractUnitOfWork(ABC):
    mascotas: AbstractRepository
    consultas: AbstractRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass
```

---

### Paso 4: Implementar un UoW en memoria

```python
# service_layer/unit_of_work.py

class InMemoryUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        from adapters.repository_memory import InMemoryRepository
        self.mascotas = InMemoryRepository()
        self.consultas = InMemoryRepository()
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        self.committed = False
```

---

### Paso 5: Caso de uso con el UoW

```python
# service_layer/handlers.py

def registrar_consulta(mascota_id, motivo, uow):
    with uow:
        mascota = uow.mascotas.get(mascota_id)
        if not mascota:
            raise ValueError("Mascota no encontrada")

        consulta = uow.consultas.add(
            Consulta(id=1, mascota_id=mascota_id, motivo=motivo)
        )
        mascota.agregar_consulta(consulta)
        uow.commit()
```

---

### 🧪 Paso 6: Pruebas iniciales (TDD)

Tu punto de partida:

```python
# tests/test_uow.py

from service_layer.unit_of_work import InMemoryUnitOfWork
from domain.models import Mascota
from service_layer.handlers import registrar_consulta

def test_commit_guarda_cambios():
    uow = InMemoryUnitOfWork()
    mascota = Mascota(id=1, nombre="Luna")
    uow.mascotas.add(mascota)

    registrar_consulta(mascota.id, "Vacunación", uow)

    assert uow.committed is True
    assert len(mascota.historial) == 1


def test_rollback_revierte_cambios():
    uow = InMemoryUnitOfWork()
    mascota = Mascota(id=1, nombre="Luna")
    uow.mascotas.add(mascota)

    try:
        registrar_consulta(999, "Desparasitación", uow)
    except ValueError:
        pass

    assert uow.committed is False
    assert len(mascota.historial) == 0
```

---

## 🚧 Restricciones

* 🧪 Usa **TDD**: escribe las pruebas antes del código que las hace pasar.
* 🧱 Aplica **Unit of Work** para coordinar los repositorios.
* 🚫 No uses librerías externas (sin SQLAlchemy por ahora).
* ✅ Mantén una **arquitectura limpia** (domain / adapters / service_layer / tests).

---

## 🎓 Nivel

**Intermedio** — Requiere conocer abstracciones, inyección de dependencias y flujo transaccional.

---

## 🏁 Criterio de éxito

El programador sabrá que resolvió correctamente el kata cuando:

* Todos los tests pasan.
* El código mantiene separación entre dominio, infraestructura y aplicación.
* El UoW coordina correctamente commits y rollbacks.

---

## 🌟 Versión extendida (opcional)

**Objetivo:**
Llevar tu UoW al mundo real usando **SQLAlchemy** y una base de datos SQLite.

**Desafío adicional:**

1. Implementa `SqlAlchemyUnitOfWork` con una sesión real.
2. Usa un repositorio SQL en lugar del repositorio en memoria.
3. Escribe un test de integración que valide que los cambios se guardan en la base de datos sólo cuando se llama `commit()`.

**Pistas:**

* Usa `session_factory = sessionmaker(bind=create_engine("sqlite:///:memory:"))`
* No olvides llamar `rollback()` en el `__exit__`.
