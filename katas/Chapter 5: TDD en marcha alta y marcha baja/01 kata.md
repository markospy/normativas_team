# 🧩 Kata: “TDD en Marcha Alta y Marcha Baja — Clínica Veterinaria”

### **Contexto:**
Basado en el capítulo *“TDD in High Gear and Low Gear”* del libro *Architecture Patterns with Python*, este ejercicio explora cómo alternar entre pruebas de bajo nivel (unidad) y alto nivel (servicios) para balancear **acoplamiento** y **retroalimentación de diseño**.

**Escenario:**
Una clínica veterinaria gestiona **consultas y vacunas**. Queremos implementar el caso de uso `asignar_cita` con un enfoque de TDD, aplicando “marcha baja” (tests sobre el dominio) y luego “marcha alta” (tests sobre el servicio).

---

### 🧪 Objetivo

1. Implementar el caso de uso `asignar_cita` donde un veterinario puede asignarse a una cita libre.
2. Practicar el cambio entre pruebas de dominio y de capa de servicio, observando el impacto en el diseño y el acoplamiento.

---

### ⚙️ Instrucciones

1. **Crea las entidades del dominio:**

   * `Veterinario(id, nombre, especialidad)`
   * `Cita(id, fecha, estado, veterinario=None)`

2. **Implementa la lógica del dominio:**

   * Método `asignar(veterinario)` en la clase `Cita`, que cambia su estado a `"asignada"` solo si estaba `"pendiente"`.

3. **Crea la capa de servicio:**
   Un módulo `services.py` con una función:

   ```python
   def asignar_cita(cita_id, veterinario_id, repo, session):
       cita = repo.obtener_cita(cita_id)
       vet = repo.obtener_veterinario(veterinario_id)
       cita.asignar(vet)
       session.commit()
   ```

4. **Define pruebas en dos niveles:**

   * **Marcha baja (low gear):** Pruebas directas sobre el dominio (`test_cita.py`)
   * **Marcha alta (high gear):** Pruebas sobre el servicio (`test_services.py`)

5. **Aplica TDD:**
   Escribe primero el test fallando, luego implementa el código hasta hacerlo pasar.

---

### ⚖️ Restricciones

* Usa **TDD** (escribe el test antes del código).
* No utilices frameworks web ni bases de datos reales (usa `FakeRepository` y `FakeSession`).
* Código limpio: sin dependencias innecesarias ni acoplamiento fuerte.

---

### 🧩 Nivel

**Intermedio:** combina conceptos de TDD, capas de dominio y servicios.

---

### 🧱 Ejemplo inicial

**Archivo:** `test_cita.py`

```python
def test_no_puede_asignar_si_ya_esta_asignada():
    vet = Veterinario(1, "Dr. López", "Felinos")
    cita = Cita(1, "2025-10-19", "asignada", vet)
    nuevo_vet = Veterinario(2, "Dra. Ramírez", "Caninos")

    with pytest.raises(ValueError):
        cita.asignar(nuevo_vet)
```

**Archivo:** `test_services.py`

```python
def test_asigna_veterinario_a_cita():
    cita = Cita(1, "2025-10-19", "pendiente")
    vet = Veterinario(1, "Dr. López", "Felinos")
    repo = FakeRepository([cita], [vet])
    session = FakeSession()

    services.asignar_cita(cita.id, vet.id, repo, session)

    assert cita.estado == "asignada"
    assert cita.veterinario == vet
```

---

### ✅ Criterio de éxito

El kata está completado cuando:

* Todos los tests pasan (dominio y servicio).
* La lógica de asignación está bien encapsulada en el dominio.
* La capa de servicio no tiene reglas de negocio, solo orquestación.
* Puedes refactorizar el dominio sin romper tests de servicio.

---

### 🚀 Versión extendida (opcional)

1. Agrega la regla: un veterinario no puede tener más de **3 citas simultáneas**.
2. Crea un test en el servicio que verifique esta restricción.
3. Refactoriza usando **un patrón Unit of Work** para simular transacciones.