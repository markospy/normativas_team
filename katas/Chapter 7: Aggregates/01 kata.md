# 🐾 **Kata: El Agregado del Paciente**

### 📘 **Contexto**

Este ejercicio surge del **Capítulo 7: Aggregates** del libro *Architecture Patterns with Python*.
El concepto clave es que un **Aggregate (Agregado)** agrupa entidades y objetos de valor que deben mantenerse **consistentes como una unidad**, con una **Aggregate Root** que actúa como el único punto de acceso y modificación.

En el contexto de una **clínica veterinaria**, queremos mantener la consistencia entre un **Paciente (Aggregate Root)** y sus **Citas (Appointments)**.
Por ejemplo, un paciente no debería tener dos citas el mismo día ni cancelar una cita inexistente.

---

## 🎯 **Objetivo del ejercicio**

Modelar el dominio de la clínica aplicando el patrón **Aggregate**, asegurando que:

* Solo se pueda modificar el estado interno del paciente a través de su **Aggregate Root**.
* Se cumplan las **invariantes** (reglas de negocio) que mantienen la consistencia del sistema.

---

## 🧱 **Instrucciones paso a paso**

1. **Crea la entidad `Appointment`:**

   * Contiene los atributos: `date`, `reason`, `status` (por defecto `"scheduled"`).
   * Puede cambiar de estado mediante un método `cancel()` que lo marque como `"cancelled"`.

2. **Crea la entidad raíz del agregado `Patient`:**

   * Tiene los atributos: `id`, `name`, y una colección privada `_appointments`.
   * Expone métodos para manipular las citas sin violar las reglas del dominio:

     * `schedule_appointment(date, reason)`
     * `cancel_appointment(date)`

3. **Define las invariantes del dominio:**

   * Un paciente **no puede tener dos citas el mismo día**.
   * Solo se puede cancelar una cita **que esté programada**.

4. **Implementa pruebas unitarias (TDD):**

   * Comienza escribiendo los tests antes de la implementación.
   * Asegúrate de probar los casos válidos y los errores esperados.

5. **Crea un repositorio mínimo (en memoria):**

   * `PatientRepository` con métodos `add(patient)` y `get(patient_id)`.

6. **Verifica que todas las operaciones sobre las citas ocurran siempre a través del `Patient`.**

---

## ⛔ **Restricciones**

* No uses librerías externas (solo `datetime` y `pytest` si deseas).
* Aplica **TDD**: primero los tests, luego el código mínimo para que pasen.
* El **Aggregate Root** debe ser el **único punto de acceso** a las citas.
* No expongas directamente la lista interna de citas (`_appointments`).

---

## ⚙️ **Nivel**

**Intermedio**, ideal para reforzar conceptos de:

* Encapsulación de dominio
* Invariantes
* Patrones DDD (Aggregate y Aggregate Root)
* Diseño orientado al comportamiento (Tell, Don’t Ask)

---

## 🧩 **Ejemplo inicial (punto de partida)**

Archivo: `test_patient_aggregate.py`

```python
from datetime import date
import pytest
from patient import Patient

def test_patient_can_schedule_an_appointment():
    patient = Patient(id=1, name="Firulais")
    patient.schedule_appointment(date(2025, 10, 20), "Vacuna antirrábica")

    assert len(patient.appointments) == 1
    assert patient.appointments[0].reason == "Vacuna antirrábica"

def test_patient_cannot_have_two_appointments_same_day():
    patient = Patient(id=2, name="Michi")
    patient.schedule_appointment(date(2025, 10, 20), "Chequeo general")

    with pytest.raises(ValueError):
        patient.schedule_appointment(date(2025, 10, 20), "Otra cita")
```

Archivo: `patient.py` (esqueleto inicial)

```python
from datetime import date

class Appointment:
    def __init__(self, date: date, reason: str):
        pass

    def cancel(self):
        pass


class Patient:
    def __init__(self, id: int, name: str):
        pass

    def schedule_appointment(self, date: date, reason: str):
        pass

    def cancel_appointment(self, date: date):
        pass
```

---

## ✅ **Criterio de éxito**

Tu solución estará completa cuando:

1. Todos los tests pasen.
2. No se pueda modificar una cita directamente fuera del `Patient`.
3. El código refleje los principios del patrón **Aggregate**:

   * Control centralizado en la raíz.
   * Consistencia de las invariantes.
   * Encapsulamiento de entidades internas.
4. El repositorio solo gestione agregados completos, no entidades sueltas.

---

## 🚀 **Versión extendida (opcional)**

Lleva el kata un paso más allá:

1. **Agrega eventos de dominio**, por ejemplo:

   * `AppointmentScheduled`
   * `AppointmentCancelled`
2. Implementa un `UnitOfWork` simple que coordine commits de varios pacientes.
3. Añade una capa de infraestructura mínima que guarde los pacientes en una base de datos SQLite (con SQLModel o SQLAlchemy).
4. Usa **dependencia explícita**: pasa el repositorio como parámetro a la función de caso de uso `schedule_appointment(patient_id, date, reason, repo)`.