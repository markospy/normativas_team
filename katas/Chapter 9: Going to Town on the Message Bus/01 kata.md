# 🧩 Kata: “Todo es un Evento” — Clínica Veterinaria

###**Contexto:**
Inspirado en el capítulo *“Going to Town on the Message Bus”* de *Architecture Patterns with Python*, este kata busca llevar el patrón *Message Bus* al corazón del dominio. En lugar de tener funciones de servicio tradicionales, toda acción —tanto interna como externa— será procesada como un evento.

---

## 🎯 Objetivo del ejercicio

Transformar una aplicación de una clínica veterinaria para que **todas las operaciones del dominio se manejen a través de eventos y handlers**, usando un bus de mensajes interno.

---

## 🧱 Instrucciones

1. **Define eventos**:

   * `PetAdmitted` — una mascota es admitida para consulta.
   * `PetTreated` — la mascota ha recibido tratamiento.
   * `PetDischarged` — la mascota fue dada de alta.

2. **Crea handlers (funciones manejadoras)** para cada evento.

   * `handle_pet_admitted(event, uow)` — registra la mascota en la base de datos.
   * `handle_pet_treated(event, uow)` — agrega un registro de tratamiento.
   * `handle_pet_discharged(event, uow)` — cambia el estado de la mascota a “alta”.

3. **Implementa un MessageBus** que:

   * Reciba un evento.
   * Encuentre el handler correspondiente.
   * Ejecute el handler.
   * Permita que los handlers emitan nuevos eventos internos.

4. **Usa un Unit of Work (UoW)** simulado (sin base de datos real) para mantener la consistencia del dominio.

---

## ⚙️ Restricciones

* No usar frameworks externos (solo `dataclasses`, `typing`, y `uuid`).
* Aplicar **TDD**: primero escribe los tests para cada evento y handler.
* Todos los flujos deben pasar por el bus (no se permite llamar handlers directamente).

---

## 🧩 Nivel

Intermedio

---

## 💡 Ejemplo inicial

```python
# domain/events.py
from dataclasses import dataclass

class Event:
    pass

@dataclass
class PetAdmitted(Event):
    pet_id: str
    name: str
    species: str

@dataclass
class PetTreated(Event):
    pet_id: str
    treatment: str

@dataclass
class PetDischarged(Event):
    pet_id: str
```

```python
# service_layer/messagebus.py
class MessageBus:
    def __init__(self, handlers):
        self.handlers = handlers

    def handle(self, event, uow):
        handler = self.handlers[type(event)]
        handler(event, uow)
```

```python
# tests/test_pet_lifecycle.py
def test_pet_lifecycle():
    event = PetAdmitted(pet_id="1", name="Luna", species="Perro")
    # TODO: inicializar bus, uow y probar el flujo
    ...
```

---

## ✅ Criterio de éxito

* Todos los tests pasan.
* Ningún servicio o capa del dominio accede a otro componente sin pasar por el `MessageBus`.
* Los handlers son funciones puras con dependencias explícitas (como el `uow`).

---

## 🚀 Versión extendida (opcional)

1. Agrega un nuevo evento: `TreatmentFailed`, que al dispararse envíe un correo (simulado) al veterinario responsable.
2. Implementa una cola de eventos pendientes dentro del `UnitOfWork`, para manejar eventos en cascada.
3. Simula un flujo completo:

   * `PetAdmitted` → `PetTreated` → `PetDischarged`
   * Donde cada paso emite el siguiente evento automáticamente.