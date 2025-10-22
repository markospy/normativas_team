# 🐾 Kata: Gestión de citas en una clínica veterinaria con Dependency Injection

### Contexto

Este ejercicio surge de los conceptos del capítulo 13 de *Architecture Patterns with Python*, donde se explica cómo aplicar **Dependency Injection** para desacoplar la lógica de negocio de las dependencias concretas (repositorios, gateways, unidades de trabajo). Aquí simularemos un **sistema de reservas de citas para mascotas**, usando DI para poder intercambiar implementaciones (por ejemplo, bases de datos reales o en memoria) y facilitar pruebas unitarias.

---

## Objetivo del ejercicio

1. Implementar un **servicio de citas** (`AppointmentService`) que permita:

   * Crear nuevas citas para mascotas.
   * Consultar todas las citas agendadas.
2. Desacoplar la lógica de negocio de la persistencia usando **Dependency Injection**, de manera que se pueda inyectar un **repositorio** diferente para pruebas.
3. Escribir **tests unitarios** que validen la funcionalidad sin depender de una base de datos real.

---

## Restricciones

* Usar **Python**.
* Aplicar **Dependency Injection** para inyectar dependencias en los servicios.
* Usar **TDD**: primero los tests, luego la implementación.
* No usar librerías externas para DI; la inyección será manual.
* Mantener el código limpio y modular, siguiendo principios de **Clean Architecture**.

---

## Nivel

**Intermedio** (requiere aplicar conceptos de DI y separar infraestructura de dominio).

---

## Escenario inicial / ejemplo de punto de partida

```python
# domain/models.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Appointment:
    pet_name: str
    owner_name: str
    date: datetime

# domain/repositories.py
from abc import ABC, abstractmethod

class AbstractAppointmentRepository(ABC):
    @abstractmethod
    def add(self, appointment: Appointment):
        ...

    @abstractmethod
    def list(self):
        ...

# services.py
class AppointmentService:
    def __init__(self, repository: AbstractAppointmentRepository):
        self.repository = repository

    # Método a implementar
    def schedule_appointment(self, pet_name: str, owner_name: str, date):
        ...

    # Método a implementar
    def get_all_appointments(self):
        ...
```

---

## Pasos del ejercicio

1. **Crear tests vacíos** usando `pytest` para los métodos `schedule_appointment` y `get_all_appointments`.
2. **Implementar un repositorio en memoria** que cumpla la interfaz `AbstractAppointmentRepository`.
3. **Inyectar el repositorio** en `AppointmentService`.
4. Implementar los métodos del servicio usando la dependencia inyectada.
5. **Escribir tests** que verifiquen:

   * Que se pueden agregar citas.
   * Que se pueden listar todas las citas.
6. Refactorizar el código para que:

   * Sea fácil reemplazar el repositorio por uno basado en base de datos real.
   * Mantenga las pruebas verdes sin tocar la lógica del servicio.

---

## Criterio de éxito

* Todos los tests pasan.
* El servicio funciona correctamente con el repositorio inyectado.
* La lógica de dominio está desacoplada de la infraestructura.
* Es posible reemplazar el repositorio sin modificar `AppointmentService`.

---

## Versión extendida (opcional)

1. Implementar un **repositorio SQLite o PostgreSQL** y probar que `AppointmentService` funciona igual.
2. Añadir validaciones:

   * No permitir citas en fechas pasadas.
   * No permitir más de una cita para la misma mascota en la misma fecha.
3. Agregar un **Message Bus** que dispare un evento `AppointmentScheduled` cada vez que se agenda una cita.
4. Integrar un **gateway de notificación por email**, inyectable, que reciba los eventos y envíe confirmaciones a los dueños.