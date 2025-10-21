# 🧩 Kata: “Commands and commands handlers” — Clínica Veterinaria

---

### 🧠 Contexto

En capítulos anteriores trabajaste con **eventos** (notificaciones de que algo ya ocurrió) y un **Message Bus** que los distribuía a suscriptores.
Este ejercicio surge del **Capítulo 10 del libro *Cosmic Python***, que introduce el concepto de **Command** como una solicitud explícita para que el sistema *haga algo*.
Mientras los eventos comunican *hechos pasados*, los comandos expresan *intenciones o acciones* que deben ejecutarse de forma confiable.

Aplicarás este concepto en el dominio de una **clínica veterinaria**, modelando comandos como “Registrar una cita”, “Actualizar información del paciente”, etc.

---

## 🎯 Objetivo del ejercicio

Implementar un **mecanismo de comandos y manejadores (Command Handlers)** en una aplicación modular, siguiendo los principios del *Message Bus pattern*.

Concretamente, deberás:

1. Definir clases de **Command** que representen acciones del sistema veterinario (por ejemplo, `RegistrarCita` o `ActualizarHistorialMedico`).
2. Implementar **handlers** (funciones o clases) que procesen esos comandos.
3. Extender el **Message Bus** existente para que:

   * Distinga entre **Command** y **Event**.
   * Envíe **Commands** a un único manejador (fail-fast si falla).
   * Despache **Events** a múltiples suscriptores (sin detener el flujo si alguno falla).
4. Usar un **Unit of Work** (real o simulado) para garantizar que los cambios en la base de datos sean atómicos.
5. Implementar pruebas unitarias (mínimas) para validar el flujo completo de un comando.

---

## ⚙️ Restricciones

* **Patrón obligatorio:** Command + Message Bus.
* **Arquitectura:** Clean / Hexagonal (puedes usar estructuras simples).
* **No usar frameworks externos** (solo `dataclasses`, `typing`, `pytest` si lo deseas).
* **Debe existir al menos un comando y un evento generado como consecuencia.**
* **TDD opcional**, pero recomendable (primero los tests, luego la implementación).

---

## 📈 Nivel

**Intermedio.**
Requiere comprensión previa del patrón Message Bus, eventos, y unidad de trabajo.

---

## 🐾 Escenario (ejemplo inicial)

Tu clínica veterinaria necesita registrar citas médicas de pacientes.
Cuando una cita se registra correctamente, el sistema debe generar un evento para enviar un recordatorio al tutor del animal.

### Código inicial

**commands.py**

```python
from dataclasses import dataclass

class Command:
    pass


@dataclass
class RegistrarCita(Command):
    id_paciente: str
    fecha: str
    motivo: str
```

**events.py**

```python
from dataclasses import dataclass

class Event:
    pass


@dataclass
class RecordatorioCitaEnviado(Event):
    id_paciente: str
    fecha: str
```

**messagebus.py (esqueleto)**

```python
def handle(message, uow):
    queue = [message]
    results = []
    while queue:
        msg = queue.pop(0)
        if isinstance(msg, Event):
            # manejar evento
            pass
        elif isinstance(msg, Command):
            # manejar comando
            pass
    return results
```

**Objetivo inicial:**
Implementar el flujo para que al enviar un `RegistrarCita`, el sistema:

1. Cree el registro de cita (simulado).
2. Genere el evento `RecordatorioCitaEnviado`.
3. El Message Bus lo despache correctamente.

---

## ✅ Criterio de éxito

El kata se considera resuelto cuando:

* Todos los comandos tienen **un único handler** asignado.
* Los handlers ejecutan su lógica sin acoplamiento a infraestructura.
* Los eventos derivados se propagan correctamente.
* El sistema distingue entre fallos en comandos (deben romper el flujo) y fallos en eventos (deben continuar).
* Los tests pasan y el código se mantiene limpio y comprensible.

**Ejemplo de test esperado:**

```python
def test_registrar_cita_dispara_evento_recordatorio():
    uow = FakeUnitOfWork()
    bus = MessageBus(uow=uow)

    command = RegistrarCita(id_paciente="DOG-123", fecha="2025-11-01", motivo="Vacunación")
    bus.handle(command)

    assert uow.citas_repo.was_created("DOG-123")
    assert any(isinstance(e, RecordatorioCitaEnviado) for e in uow.collect_new_events())
```

---

## 🚀 Versión extendida (opcional)

Lleva el ejercicio un paso más allá:

1. Implementa una **reintento automático** para el envío de eventos fallidos (usa `tenacity` o un decorador propio de “retry”).
2. Añade un segundo comando: `CancelarCita`, que debe generar un evento `CitaCancelada`.
3. Permite que los eventos se envíen de forma **asíncrona** (por ejemplo, en una cola simulada).
4. Registra los logs de fallos de comandos vs. eventos (demostrando su diferencia de gravedad).