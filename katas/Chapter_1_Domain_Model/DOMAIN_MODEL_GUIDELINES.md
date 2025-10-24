# 🧭 DOMAIN_MODEL_GUIDELINES.md

## 🎯 Propósito

Asegurar que el **modelo de dominio** refleje la lógica del negocio, manteniéndose **independiente de frameworks, bases de datos o infraestructura**.

---

## 🧩 Principios Clave

1. **Dominio puro**

   * Sin dependencias externas (`sqlalchemy`, `fastapi`, etc.).
   * Solo usa Python estándar (`dataclasses`, `datetime`, `typing`).

2. **Tipado**
   * Tipado de estructuras de datos complejas.

   ```python
   # Evita esto:
   self._appointments = set() # no tienes autocompletado, es menos claro sobre la utilidad de la estructura de datos

   # Prefiere esto:
   self._appointments: set[AppointmentRequest] = set() # obtienes autocompletado, es más claro sobre la utilidad de la estructura de datos
   ```

3. **Modela comportamientos, no datos**

   * Las entidades deben tener lógica (métodos que expresen reglas del negocio).
   * Evita que sean solo contenedores de atributos.

4. **Entidades y objetos de valor**

   * Entidades → tienen identidad (`Veterinarian`, `Appointment`).
   * Value Objects → inmutables y sin identidad (`Specialty`, `DateRange`).
   * Claridad conceptual:
      * **Las entidades DEBEN tener un `id` único** para mantener su identidad a través del ciclo de vida.
      * **Los value objects NO deben tener `id`** ya que se identifican por su valor, no por identidad.

   ```python
   # ✅ Entidad con identidad
   class Veterinarian:
       def __init__(self, name: str, specialty: str, max_daily_appointments: int):
           self.id = uuid4()  # Identidad única
           self.name = name
           self.specialty = specialty
           self.max_daily_appointments = max_daily_appointments

   # ✅ Value Object sin identidad
   class Specialty:
       def __init__(self, name: str):
           self.name = name  # Se identifica por su valor
   ```

   * **Usa el `id` en lógica de negocio** cuando sea relevante (retornar entidad asignada, definir y comparar identidades).
   * **NO agregues `id` solo por agregarlo** - debe tener propósito en el dominio.

5. **Reglas del negocio en el dominio**

   * Las validaciones y excepciones de negocio viven aquí (`NoAvailableVet`, `OverbookedVet`).
   * Al crear excepciones existe una clase padre que define capa de origen de la excepción. Las excepciones hijas deben son explicitas con la causa de la excepcion, con un nombre de clase y un mensaje claro y conciso sobre la causa. Se prefiere tener el mensaje por defecto en la declaracion de la clase.

   ```python
   class DomainError(Exception):
      pass


   class NoAvailableVet(DomainError): # Nombre de excepción claro
      """Excepción lanzada cuando no hay veterinarios disponibles."""
      message = "No available vet" # mensaje por default

      def __init__(self, message: str = None): # puedes o no personalizar el mensaje al lanzar la excepcion. Más flexibilidad.
         super().__init__(message or self.message)

   ```

6. **Separación de responsabilidades de validación**

   * **Validaciones de formato** (longitud de strings, tipos de datos, formatos de fecha) pertenecen a la **capa de infraestructura** (Pydantic, FastAPI).
   * **Reglas de negocio** (lógica de asignación, restricciones de dominio, excepciones semánticas) pertenecen al **dominio**.
   * El dominio NO debe validar formatos de entrada, solo aplicar reglas de negocio.

   ```python
   # ❌ NO en el dominio - validaciones de formato
   def __init__(self, name: str):
       if len(name) < 2:  # Esto va en infraestructura
           raise ValueError("Name too short")

   # ✅ SÍ en el dominio - reglas de negocio
   def assign_appointment(self, appointment: AppointmentRequest):
       if not self.can_accept_appointment(appointment):  # Regla de negocio
           raise OverbookedVet("Cannot accept more appointments")
   ```

7. **Independencia de infraestructura**

   * El dominio no importa de `infrastructure/` ni de `interfaces/`.
   * La infraestructura adapta al dominio, no al revés.

8. **Lenguaje ubicuo**

   * Usa nombres del negocio, no técnicos (`allocate_appointment()`, no `process_data()`).

9. **TDD y simplicidad**

   * Prueba toda lógica de dominio sin base de datos ni frameworks.
   * Tests expresan reglas del negocio, no detalles técnicos.

---

## 📂 Estructura sugerida

```
/domain
  ├── models.py
  ├── services.py
  └── exceptions.py
```

> Ningún archivo en `domain/` puede importar desde `infrastructure/` o `interfaces/`.

---

## ✅ Checklist rápido (antes de aprobar o crear un PR)

* [ ] El dominio no usa frameworks.
* [ ] Las reglas del negocio están dentro del dominio.
* [ ] Los nombres reflejan el lenguaje del negocio.
* [ ] Se lanzan errores semánticos, evitando la clase ValueError.
* [ ] Los tests cubren las reglas de negocio.
* [ ] Las validaciones de formato están en infraestructura, no en el dominio.
* [ ] El dominio solo contiene reglas de negocio puras.
* [ ] Las entidades tienen `id` único, los value objects no.
* [ ] Los `id` se usan en lógica de negocio cuando es relevante.