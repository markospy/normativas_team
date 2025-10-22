# 🧩 **Kata: “Abstracciones en la Clínica Veterinaria”**

---

### 🧠 **Contexto**

Este ejercicio surge del estudio del capítulo **“Abstractions”** del libro *Cosmic Python*, donde se introduce la idea de **separar el dominio de la infraestructura** mediante **interfaces o clases abstractas**.
En lugar de que tu dominio dependa de una base de datos concreta (como SQLAlchemy), definimos una **abstracción (`AbstractRepository`)** que puede tener diferentes implementaciones (SQL, Mongo, in-memory, etc.).

Tu misión será aplicar ese concepto al dominio de una **clínica veterinaria** 🐶🐱, donde gestionaremos la asignación de **citas médicas** a los **veterinarios disponibles**.

---

## 🎯 **Objetivo del ejercicio**

Diseñar un modelo de dominio simple para manejar **citas veterinarias**, y desacoplarlo de la infraestructura mediante una **abstracción del repositorio**.

El flujo principal será:

1. Crear entidades del dominio (`Veterinario`, `Cita`, `Mascota`).
2. Implementar un **AbstractRepository**.
3. Crear una versión **FakeRepository** (para pruebas) y otra **InMemoryRepository** (de ejemplo).
4. Escribir un test que verifique que el **dominio no depende de la implementación concreta del repositorio**.

---

## ⚙️ **Instrucciones paso a paso**

1. **Crea las entidades del dominio:**

   * `Veterinario`: con nombre, especialidad, lista de citas asignadas.
   * `Cita`: con fecha, hora, mascota, y estado (“pendiente”, “completada”).
   * `Mascota`: con nombre, especie, y dueño.

2. **Define una interfaz de repositorio:**

   * Clase abstracta `AbstractRepository` (usa `abc.ABC`).
   * Métodos abstractos:

     ```python
     add(self, entity)
     get(self, id)
     list(self)
     ```

3. **Implementa dos versiones concretas:**

   * `InMemoryRepository`: usa una lista interna para almacenar entidades.
   * `FakeRepository`: simula datos preexistentes (útil en tests).

4. **Escribe un servicio de dominio:**

   * Función `agendar_cita(vet_repo, cita)`
     → busca un veterinario disponible y le asigna la cita.

5. **Crea tests usando el repositorio fake:**

   * Testea que `agendar_cita()` funcione igual sin importar si se usa `InMemoryRepository` o `FakeRepository`.

---

## 🧩 **Restricciones**

* Usa **Python puro**, sin frameworks externos (solo `abc`, `pytest` si deseas).
* Aplica **TDD**: escribe primero los tests antes de implementar cada clase.
* Mantén el **dominio libre de dependencias** (sin referencias a bases de datos, ORM, etc.).
* Respeta los principios de **Clean Architecture**:

  * Dominio → no depende de infraestructura.
  * Repositorio es una abstracción.
  * Implementaciones concretas son adaptadores.

---

## 📈 **Nivel:** Intermedio

(ideal para reforzar el dominio, abstracciones e inyección de dependencias).

---

## 🧪 **Ejemplo inicial (punto de partida)**

```python
# test_agendar_cita.py

from datetime import datetime
from domain import Cita, Mascota, Veterinario
from repository import FakeRepository
from services import agendar_cita

def test_agendar_cita_asigna_correctamente():
    # Arrange
    vet = Veterinario(nombre="Dra. López", especialidad="Felinos")
    repo = FakeRepository([vet])
    mascota = Mascota(nombre="Michi", especie="Gato", dueño="Carlos")
    cita = Cita(fecha=datetime(2025, 10, 20), mascota=mascota)

    # Act
    agendar_cita(repo, cita)

    # Assert
    assert cita in vet.citas
```

---

## ✅ **Criterio de éxito**

Sabrás que el kata está resuelto correctamente cuando:

1. Todos los tests pasan (usando `FakeRepository` y `InMemoryRepository`).
2. Ninguna parte del dominio importa módulos de infraestructura.
3. Puedes cambiar la implementación del repositorio sin tocar el código del dominio.
4. El código es legible, con nombres claros y sin dependencias ocultas.

---

## 🚀 **Versión extendida (opcional)**

Lleva el ejercicio un paso más allá:

1. Implementa una versión `SqlAlchemyRepository` (simulada o real).
2. Agrega validaciones de negocio (por ejemplo:

   * Un veterinario no puede tener más de 3 citas en el mismo día).
3. Usa **inyección de dependencias** en el servicio `agendar_cita()` para seleccionar dinámicamente el repositorio (por configuración o argumento).
4. Añade un test doble (mock o spy) para verificar que se llama correctamente al método `add()` del repositorio.