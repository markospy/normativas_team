# 🧩 Kata: “Asignación de Consultas Veterinarias — Aplicando la Service Layer”

---

### 🧠 Contexto

Este ejercicio surge del **capítulo 4 de *Cosmic Python***, donde se introduce la **capa de servicios (Service Layer)** como una forma de separar la lógica de aplicación (use cases) de la capa de infraestructura (HTTP, base de datos, etc.).
En ese capítulo, se muestra cómo los endpoints HTTP empiezan a llenarse de lógica de negocio y orquestación, y cómo extraer esa lógica a una capa de servicios mejora la claridad, el testeo y la mantenibilidad.

En este kata adaptaremos el ejemplo al dominio de una **clínica veterinaria**, aplicando estos mismos principios.

---

## 🎯 Objetivo

Implementar una **capa de servicio** que gestione la asignación de **consultas veterinarias** a los veterinarios disponibles, manteniendo las responsabilidades separadas entre:

* **Dominio** → lógica pura del negocio (entidades, reglas de asignación).
* **Repositorio** → acceso a los datos (abstracción de persistencia).
* **Service Layer** → orquestación del caso de uso (“Asignar una consulta”).
* **Entrypoint (simulado)** → interfaz que llama al servicio.

---

## ⚙️ Instrucciones paso a paso

1. **Modela el dominio**
   Crea una entidad `Veterinario` y una entidad `Consulta`.

   * Un veterinario tiene un `nombre`, una `especialidad` y una lista de `consultas_asignadas`.
   * Una consulta tiene un `id`, una `especie` (perro, gato, ave, etc.) y un `estado` (`pendiente`, `asignada`, `atendida`).

2. **Define la lógica del dominio (regla de negocio)**
   Implementa una función de dominio `asignar_consulta(veterinarios, consulta)` que:

   * Asigne la consulta al primer veterinario con la especialidad adecuada y con menos de 3 consultas activas.
   * Lance una excepción `SinVeterinarioDisponible` si nadie cumple las condiciones.

3. **Crea la abstracción del repositorio**
   Define una clase abstracta `AbstractRepository` con los métodos:

   * `add(veterinario)`
   * `get(nombre)`
   * `list()`

   Luego implementa una versión **en memoria (FakeRepository)** para los tests.

4. **Implementa la capa de servicio (`services.py`)**
   Define una función:

   ```python
   def asignar_consulta(consulta, repo, session):
       veterinarios = repo.list()
       try:
           asignado_a = model.asignar_consulta(veterinarios, consulta)
           session.commit()
           return asignado_a.nombre
       except model.SinVeterinarioDisponible as e:
           raise e
   ```

5. **Simula un entrypoint (controlador HTTP, CLI, etc.)**
   Implementa un script o función que reciba los datos de una nueva consulta y llame al servicio `asignar_consulta`.

6. **Prueba con TDD**
   Escribe primero un test que compruebe que:

   * Si hay un veterinario disponible con la especialidad correcta, se asigna correctamente.
   * Si no hay veterinario disponible, se lanza la excepción `SinVeterinarioDisponible`.

---

## 🚫 Restricciones

* Usa **Python puro**, sin frameworks externos (sin Flask, sin ORM).
* Usa **TDD**: primero los tests, luego las implementaciones.
* Mantén separadas las capas en módulos: `domain/`, `service_layer/`, `adapters/`, `tests/`.
* No pongas lógica de negocio en el servicio ni en los endpoints (solo orquestación).

---

## 🧩 Nivel

**Intermedio** — requiere conocer conceptos de DDD (modelo de dominio), repositorios y separación de capas.

---

## 💡 Ejemplo inicial (punto de partida)

Estructura de carpetas:

```
veterinaria/
├── domain/
│   ├── __init__.py
│   └── model.py
├── service_layer/
│   ├── __init__.py
│   └── services.py
├── adapters/
│   ├── __init__.py
│   └── repository.py
└── tests/
    └── test_asignacion.py
```

Código base mínimo:

```python
# domain/model.py
class SinVeterinarioDisponible(Exception):
    pass


class Veterinario:
    def __init__(self, nombre, especialidad):
        self.nombre = nombre
        self.especialidad = especialidad
        self.consultas_asignadas = []

    def puede_tomar_consulta(self, consulta):
        return (
            self.especialidad == consulta.especie
            and len(self.consultas_asignadas) < 3
        )


class Consulta:
    def __init__(self, id, especie):
        self.id = id
        self.especie = especie
        self.estado = "pendiente"


def asignar_consulta(veterinarios, consulta):
    for v in veterinarios:
        if v.puede_tomar_consulta(consulta):
            v.consultas_asignadas.append(consulta)
            consulta.estado = "asignada"
            return v
    raise SinVeterinarioDisponible()
```

Y un test inicial:

```python
# tests/test_asignacion.py
from veterinaria.domain import model
from veterinaria.service_layer import services


class FakeRepository:
    def __init__(self, veterinarios):
        self._veterinarios = set(veterinarios)

    def list(self):
        return list(self._veterinarios)


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True


def test_asigna_consulta_a_veterinario_disponible():
    vet = model.Veterinario("Dra. Ana", "perro")
    repo = FakeRepository([vet])
    session = FakeSession()
    consulta = model.Consulta("c-1", "perro")

    asignado = services.asignar_consulta(consulta, repo, session)

    assert asignado == "Dra. Ana"
    assert consulta.estado == "asignada"
    assert session.committed
```

---

## ✅ Criterio de éxito

El kata se considera completado si:

* Todos los tests pasan correctamente.
* La capa de servicio **no contiene lógica de negocio** (solo orquesta).
* Las entidades del dominio están **libres de dependencias externas**.
* El código mantiene una estructura limpia y coherente entre capas.

---

## 🚀 Versión extendida (opcional)

Lleva el ejercicio un paso más allá:

1. **Introduce Unit of Work**: encapsula `repo` y `session` en un `UoW` para que el servicio quede más limpio.
2. **Agrega un endpoint HTTP con FastAPI o Flask** que reciba consultas y llame a la capa de servicio.
3. **Agrega eventos de dominio**: por ejemplo, cuando se asigna una consulta, dispara un evento `ConsultaAsignada` que podría usarse para notificar al cliente.