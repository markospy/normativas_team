# **Kata práctico** correspondiente al **Capítulo 8: *Events and Message Bus*** de *Architecture Patterns with Python*, adaptado al dominio de una **clínica veterinaria**.

---

## 🧭 **Contexto**

Este ejercicio surge del estudio del capítulo *“Events and the Message Bus”* del libro *Cosmic Python*, donde se propone **manejar los efectos secundarios** de las acciones del dominio usando **eventos de dominio** y un **bus de mensajes**.

En una clínica veterinaria, cada evento clínico (consulta, cirugía, vacunación, etc.) puede tener **efectos colaterales**: enviar un recordatorio al dueño, actualizar el historial médico o notificar al laboratorio.
Si esos efectos se mezclan dentro del dominio, el código se vuelve acoplado y difícil de mantener.

Con los **Domain Events** y el **Message Bus**, separarás la lógica del dominio (lo que *ocurre*) de los efectos secundarios (lo que *debe hacerse después*).

---

## 🎯 **Objetivo del ejercicio**

Implementar un sistema sencillo para una **clínica veterinaria** que gestione **consultas médicas de mascotas**, y donde cada vez que se crea una consulta:

* se registre un evento de dominio `ConsultaCreada`,
* y el sistema lo despache automáticamente a uno o más *handlers* (por ejemplo, enviar recordatorio al dueño o registrar puntos en el programa de fidelidad).

---

## 🧩 **Instrucciones paso a paso**

1. **Define el modelo de dominio**

   * Crea una clase `Consulta` que represente una consulta veterinaria con los atributos:

     * `id`, `mascota`, `veterinario`, `motivo`, `fecha`.
   * Agrega una lista interna `events` para registrar los eventos generados por el agregado.

2. **Crea el evento de dominio**

   * Define una clase `ConsultaCreada` que herede de una clase base `Event`.
   * Usa `@dataclass` para representar el evento y sus datos (por ejemplo, `mascota`, `veterinario`, `fecha`).

3. **Genera el evento desde el dominio**

   * En el constructor o método de fábrica de `Consulta`, agrega una instancia de `ConsultaCreada` a la lista `events`.

4. **Implementa un Message Bus simple**

   * Crea un módulo `messagebus.py` con una función `handle(event)` que busca los *handlers* registrados para el tipo de evento.
   * Ejemplo: un diccionario `HANDLERS = {ConsultaCreada: [notificar_dueño, registrar_fidelidad]}`.

5. **Crea los handlers**

   * Implementa funciones *handler* simples:

     * `notificar_dueño(event)` imprime `"📧 Enviando recordatorio al dueño de {event.mascota}"`.
     * `registrar_fidelidad(event)` imprime `"⭐ Sumando puntos para {event.mascota}"`.

6. **Integra con la Unidad de Trabajo (UoW)**

   * Crea una clase `UnitOfWork` que simule el patrón (no necesita DB real).
   * Debe tener:

     * una lista `vistas` o `seen` para los objetos de dominio manipulados.
     * método `commit()` que llama internamente a `publish_events()` → este a su vez ejecuta los handlers usando el bus.

7. **Prueba el flujo**

   * Crea una nueva `Consulta`, registra el objeto en el `UnitOfWork`, haz `commit()` y observa cómo se ejecutan los handlers.

---

## 🚦 **Restricciones**

* Usa **Python 3.10+**.
* **No uses librerías externas** (solo `dataclasses`).
* Sigue el enfoque de **TDD**:

  * Escribe primero un test para verificar que al crear una consulta se genera un evento `ConsultaCreada`.
  * Luego otro test para verificar que al hacer `commit()`, los handlers se ejecutan.
* Mantén la **lógica de negocio limpia**, sin llamadas directas a infraestructura (ni prints dentro del dominio).

---

## 🧠 **Nivel**

🔹 **Intermedio**
Combina conceptos de **arquitectura limpia**, **eventos de dominio** y **patrón Message Bus**, aplicados en un contexto realista.

---

## 🧱 **Ejemplo inicial (punto de partida)**

Archivo `test_consultas.py`:

```python
from domain.model import Consulta
from service_layer.unit_of_work import UnitOfWork
from service_layer import messagebus

def test_evento_generado_y_despachado():
    consulta = Consulta(id=1, mascota="Luna", veterinario="Dr. Rojas", motivo="Vacunación", fecha="2025-10-19")
    uow = UnitOfWork()
    uow.register(consulta)
    uow.commit()

    # Esperado: los handlers del evento ConsultaCreada se ejecutan
    # (por ahora imprimen mensajes)
```

Archivo `domain/model.py` (borrador inicial):

```python
from dataclasses import dataclass
from domain import events

@dataclass
class Consulta:
    id: int
    mascota: str
    veterinario: str
    motivo: str
    fecha: str

    def __post_init__(self):
        self.events = []
        self.events.append(events.ConsultaCreada(self.mascota, self.veterinario, self.fecha))
```

Archivo `domain/events.py`:

```python
from dataclasses import dataclass

class Event:
    pass

@dataclass
class ConsultaCreada(Event):
    mascota: str
    veterinario: str
    fecha: str
```

---

## ✅ **Criterio de éxito**

Tu solución estará completa si:

1. Al crear una `Consulta`, se genera automáticamente un evento `ConsultaCreada`.
2. El `UnitOfWork` publica los eventos durante el `commit()`.
3. Los handlers definidos son ejecutados correctamente por el `MessageBus`.
4. Todo el código pasa los tests y respeta la separación de responsabilidades.
   (El dominio no llama directamente a infraestructura.)

---

## 🚀 **Versión extendida (opcional)**

Si quieres llevar el kata un paso más allá:

1. Implementa un **segundo evento** `VacunaAplicada` y su handler (por ejemplo, registrar en el historial médico).
2. Haz que un handler dispare otro evento (ej. `ConsultaCreada` → `VacunaAplicada`), y maneja el flujo de *eventos encadenados*.
3. Cambia el bus para procesar los eventos de forma **asíncrona** (usando `asyncio`).
4. Conecta el bus con una cola real (RabbitMQ, Redis, etc.) como simulación de un sistema distribuido.