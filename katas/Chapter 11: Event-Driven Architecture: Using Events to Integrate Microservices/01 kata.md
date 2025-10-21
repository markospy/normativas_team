# 🐾 Kata: Integración de Eventos Externos en una Clínica Veterinaria

### Contexto

Este ejercicio se basa en el capítulo 11 del libro *Architecture Patterns with Python*, donde se explora cómo integrar sistemas mediante eventos asíncronos en una arquitectura dirigida por eventos (EDA). En el contexto de una clínica veterinaria, esto puede aplicarse para integrar sistemas de gestión de citas, inventarios de medicamentos, historial médico de pacientes, entre otros.

---

## 🎯 Objetivo

Implementar un sistema que:

1. Reciba eventos externos, como la llegada de un nuevo paciente o la actualización del historial médico de un paciente.
2. Procese estos eventos y actualice el estado interno del sistema.
3. Publique eventos internos que puedan ser consumidos por otros sistemas o servicios.

---

## 🛠️ Instrucciones

1. **Configura el entorno**:

   * Instala Redis para la mensajería pub/sub.
   * Instala las librerías necesarias en Python: `redis`, `pydantic`, `pytest`.

2. **Define los eventos**:

   * Crea clases para representar los eventos que tu sistema manejará.
   * Utiliza `pydantic` para la validación de datos.

3. **Implementa el adaptador de entrada**:

   * Crea una función que se suscriba a un canal de Redis y procese los eventos entrantes.

4. **Implementa el adaptador de salida**:

   * Crea una función que publique eventos en un canal de Redis.

5. **Desarrolla el manejador de eventos**:

   * Crea funciones que manejen la lógica de negocio al recibir eventos.

6. **Escribe pruebas**:

   * Utiliza `pytest` para escribir pruebas que aseguren el correcto funcionamiento de tu sistema.

---

## 🚧 Restricciones

* Aplica los principios de arquitectura dirigida por eventos.
* Utiliza TDD (Test-Driven Development).
* No utilices frameworks web como Flask o Django; enfócate en la lógica de negocio y la integración de eventos.
* Implementa idempotencia en el manejo de eventos.

---

## 📊 Nivel

Intermedio.

---

## 🐍 Lenguaje

Python 3.8+

---

## 🧪 Ejemplo Inicial

```python
# events.py
from pydantic import BaseModel

class NewPatientEvent(BaseModel):
    patient_id: str
    name: str
    species: str
    breed: str
    age: int
```

```python
# handlers.py
from events import NewPatientEvent

def handle_new_patient(event: NewPatientEvent):
    # Lógica para manejar el evento de un nuevo paciente
    print(f"Nuevo paciente: {event.name}, {event.species}")
```

```python
# adapters.py
import redis
import json
from handlers import handle_new_patient
from events import NewPatientEvent

def subscribe_to_events():
    r = redis.Redis()
    pubsub = r.pubsub()
    pubsub.subscribe('new_patient')
    for message in pubsub.listen():
        if message['type'] == 'message':
            event_data = json.loads(message['data'])
            event = NewPatientEvent(**event_data)
            handle_new_patient(event)
```

```python
# test_handlers.py
from handlers import handle_new_patient
from events import NewPatientEvent

def test_handle_new_patient():
    event = NewPatientEvent(patient_id="123", name="Fido", species="Canine", breed="Labrador", age=5)
    handle_new_patient(event)
    # Asegúrate de que la lógica de negocio se ejecute correctamente
```

---

## ✅ Criterios de Éxito

- Todos los tests pasan correctamente.
- El sistema maneja eventos de manera asíncrona y sincrónica según sea necesario.
- Se implementa idempotencia en el manejo de eventos.
- El código sigue los principios de arquitectura dirigida por eventos.

---

## 🔁 Versión Extendida (Opcional)

Para quienes deseen profundizar:

- Implementa un sistema de notificaciones para alertar al personal veterinario sobre eventos críticos.
- Integra un sistema de persistencia para almacenar el historial médico de los pacientes.
- Implementa un sistema de autenticación y autorización para controlar el acceso a los eventos.
- Utiliza un framework de pruebas como `pytest` para asegurar la calidad del código.
