# 🧩 **Kata: Modelo de Dominio para Asignación de Citas Veterinarias**

---

### 🧠 **Contexto**

Este ejercicio nace del concepto de **Domain Model** explicado en *Cosmic Python*.
El objetivo es aprender a **modelar la lógica de negocio de forma pura**, sin depender de frameworks, bases de datos o infraestructura, enfocándonos solo en **las reglas y el comportamiento del dominio**.

Así como el libro usa una empresa de distribución para modelar la asignación de pedidos a lotes, aquí usaremos **una clínica veterinaria** que debe **asignar citas a veterinarios según disponibilidad y especialidad**.

---

## 🎯 **Objetivo**

Diseñar las clases principales del dominio para gestionar la **asignación de citas** en una clínica veterinaria:

* Un cliente solicita una cita para su mascota (por ejemplo, “chequeo general para perro” o “consulta felina”).
* La clínica tiene varios veterinarios, cada uno con una **especialidad** y **horarios disponibles**.
* El sistema debe **asignar automáticamente la cita** al veterinario adecuado según:

  1. Que tenga la **especialidad correcta**.
  2. Que tenga **espacio disponible** ese día.
  3. Que la **asignación siga las reglas de prioridad** (por ejemplo, preferir veterinarios con menor carga de trabajo).

---

## 🧱 **Instrucciones paso a paso**

### Paso 1️⃣ — Crear las entidades base

Crea las clases de dominio:

* `AppointmentRequest` → representa una solicitud de cita (cliente, mascota, especialidad, fecha).
* `Veterinarian` → representa un veterinario con su especialidad y citas asignadas.

Ejemplo:

```python
class AppointmentRequest:
    def __init__(self, client_name: str, pet_name: str, specialty: str, date):
        self.client_name = client_name
        self.pet_name = pet_name
        self.specialty = specialty
        self.date = date
```

```python
class Veterinarian:
    def __init__(self, name: str, specialty: str, max_daily_appointments: int):
        self.name = name
        self.specialty = specialty
        self.max_daily_appointments = max_daily_appointments
        self._appointments = set()
```

---

### Paso 2️⃣ — Agregar comportamiento de negocio

Implementa los métodos:

* `can_accept(appointment: AppointmentRequest) -> bool`

  * Solo si la especialidad coincide.
  * Solo si no ha alcanzado su límite de citas diarias.
* `assign(appointment: AppointmentRequest)`

  * Asigna la cita si `can_accept()` es `True`.

---

### Paso 3️⃣ — Crear la función de asignación global

Crea una función `allocate_appointment(appointment, veterinarians)` que:

* Recorra los veterinarios ordenados por menor número de citas asignadas.
* Asigne la cita al primero que cumpla las condiciones.
* Si ninguno puede, lance una excepción `NoAvailableVet`.

---

### Paso 4️⃣ — Escribir tests primero (TDD)

Crea un archivo `test_domain_model.py` con tests como:

```python
def test_assigning_to_a_vet_reduces_available_slots():
    vet = Veterinarian("Dra. López", "canina", max_daily_appointments=3)
    appointment = AppointmentRequest("Marcos", "Firulais", "canina", "2025-10-18")

    vet.assign(appointment)

    assert len(vet._appointments) == 1
```

Otros casos:

* No puede asignar si la especialidad no coincide.
* No puede asignar si ya alcanzó el máximo diario.
* La función `allocate_appointment()` elige correctamente el veterinario con menos carga.

---

## ⚙️ **Restricciones**

* 🧩 Solo puedes usar **Python estándar** (sin frameworks ni ORMs).
* 🧪 Implementa usando **TDD**: primero el test, luego el código.
* 🚫 No usar persistencia, FastAPI ni librerías externas.
* 🧼 Mantén el dominio limpio: sin `print()`, sin lógica de infraestructura.

---

## 📊 **Nivel**

**Intermedio.**
El kata combina diseño orientado a objetos, modelado de dominio y práctica de TDD.

---

## 🧩 **Ejemplo inicial (escenario de arranque)**

Archivo `test_domain_model.py`:

```python
from domain_model import Veterinarian, AppointmentRequest, allocate_appointment, NoAvailableVet

def test_assigning_to_a_vet_reduces_available_slots():
    vet = Veterinarian("Dra. López", "canina", max_daily_appointments=3)
    appointment = AppointmentRequest("Marcos", "Firulais", "canina", "2025-10-18")

    vet.assign(appointment)

    assert len(vet._appointments) == 1
```

Archivo `domain_model.py` (vacío para que empieces desde cero):

```python
# TODO: Implementar clases y lógica aquí
```

---

## ✅ **Criterio de éxito**

Sabes que resolviste correctamente el kata cuando:

1. ✅ Todos los tests pasan.
2. 🧠 La lógica de negocio (reglas) está completamente contenida en las clases de dominio.
3. 🚫 No hay dependencias externas (sin base de datos, frameworks o librerías de terceros).
4. 🧼 El código es limpio, fácil de leer y modificar.

---

## 🚀 **Versión extendida (opcional)**

### Nivel avanzado

Agrega reglas adicionales al modelo, por ejemplo:

* Un veterinario puede tener varias **especialidades secundarias**.
* Algunas citas requieren **equipamiento especial** (por ejemplo, rayos X), que solo ciertos veterinarios pueden usar.
* Implementa un **servicio de dominio** (clase aparte) que calcule automáticamente la **distribución diaria de carga de trabajo**.

**Ejemplo de extensión:**

```python
class VetSchedulerService:
    def suggest_best_vet(self, appointment: AppointmentRequest, vets: list[Veterinarian]):
        # lógica más compleja para priorizar
        ...
```
