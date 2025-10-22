# 🐾 Kata: Gestión de citas y consultas en una clínica veterinaria con CQRS

### **Contexto**

Este ejercicio surge del Capítulo 12 de *Cosmic Python*, que introduce **CQRS**. La idea es que en sistemas complejos podemos separar la **lógica de negocio y comandos** (crear, modificar o eliminar entidades) de las **consultas o vistas** (leer información de manera rápida).
En este kata, aplicaremos CQRS al dominio de una clínica veterinaria, donde tenemos pacientes (mascotas) y citas. El objetivo es **modificar datos a través de comandos** y **leer información mediante consultas separadas**, sin que la lógica de negocio se mezcle con las vistas.

---

## **Instrucciones claras**

1. **Definir el dominio y agregados**

   * Crear clases para `Mascota` y `Cita`.
   * Las `Citas` deben estar asociadas a una `Mascota`.
   * Aplicar reglas de negocio mínimas:

     * No se pueden agendar dos citas para la misma mascota al mismo tiempo.
     * Cada cita tiene fecha y hora, duración y motivo.

2. **Implementar Commands y Handlers**

   * `AgregarMascotaCommand` → Handler para agregar una mascota.
   * `AgendarCitaCommand` → Handler para crear una cita.
   * Estos handlers deben actualizar un **repositorio en memoria** (simulando persistencia).

3. **Separar las Queries**

   * Crear funciones de lectura que no usen la lógica de negocio de los comandos.
   * Ejemplos:

     * `listar_mascotas()`
     * `listar_citas_por_fecha(fecha)`
   * Las consultas deben retornar **estructuras simples** (diccionarios o listas de diccionarios).

4. **Implementar pruebas unitarias**

   * Usar `pytest`.
   * Crear tests para:

     * Agregar mascotas.
     * Agendar citas.
     * Verificar que las consultas devuelven los datos correctos.

---

## **Restricciones**

* Debes usar **TDD**: primero escribe los tests, luego el código.
* Aplica **CQRS** separando completamente Commands y Queries.
* No usar librerías externas para la persistencia (repositorio en memoria).
* Mantener el **modelo de dominio limpio**, sin consultas SQL ni filtros dentro de los agregados.

---

## **Nivel**

* Intermedio.

---

## **Ejemplo inicial**

```python
# dominio.py
from datetime import datetime

class Mascota:
    def __init__(self, nombre, especie):
        self.nombre = nombre
        self.especie = especie

class Cita:
    def __init__(self, mascota, fecha_hora, duracion, motivo):
        self.mascota = mascota
        self.fecha_hora = fecha_hora
        self.duracion = duracion
        self.motivo = motivo

# commands.py
class AgregarMascotaCommand:
    def __init__(self, nombre, especie):
        self.nombre = nombre
        self.especie = especie

class AgendarCitaCommand:
    def __init__(self, mascota_nombre, fecha_hora, duracion, motivo):
        self.mascota_nombre = mascota_nombre
        self.fecha_hora = fecha_hora
        self.duracion = duracion
        self.motivo = motivo

# queries.py
def listar_mascotas():
    return []

def listar_citas_por_fecha(fecha):
    return []

# tests/test_clinica.py
def test_agregar_mascota():
    pass  # test a implementar

def test_agendar_cita():
    pass  # test a implementar

def test_listar_citas_por_fecha():
    pass  # test a implementar
```

---

## **Criterio de éxito**

* Todos los tests pasan.
* Los comandos modifican correctamente el estado del repositorio en memoria.
* Las consultas devuelven los datos correctos sin depender del dominio.
* Se mantiene **separación clara** entre Commands y Queries.

---

## **Versión extendida (opcional)**

* Implementar un **Message Bus** simple para disparar eventos después de agendar citas (por ejemplo, `CitaAgendadaEvent`).
* Usar los eventos para **actualizar un modelo de lectura cacheado**.
* Permitir consultas más complejas:

  * Listar todas las citas de una mascota.
  * Buscar mascotas por especie.
* Simular conflictos de citas y lanzar excepciones si la regla de negocio se viola.