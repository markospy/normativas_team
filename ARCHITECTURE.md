## ⚠️ Esta guia no esta concluida. Aun no debería tomarse como guia de trabajo. En cambio nuestra guia principal es el libro [Architecure Patterns with Python](https://www.cosmicpython.com/book/preface.html)

[🧩 PARTE 1: Desarrollo detallado — Filosofía y estructura](#-parte-1---desarrollo-detallado--filosofía-y-estructura)

[🧩 PARTE 2: CAPA DE DOMINIO](#-parte-2-capa-de-dominio)

[⚙️ PARTE 3: CAPA DE APLICACIÓN](#️-parte-3-capa-de-aplicación)

[🧱 PARTE 4: CAPA DE INFRAESTRUCTURA](#-parte-4-capa-de-infraestructura)

[🧩 PARTE 5: Estructura base del módulo `interfaces`](#-parte-5-estructura-base-del-módulo-interfaces)

[🧩 PARTE 6: Testing en Clean Architecture](#-parte-6--testing-en-clean-architecture)

[⚙️ PARTE 7: Creación y Manejo de Excepciones Semánticas en Clean Architecture](#️-parte-7-creación-y-manejo-de-excepciones-semánticas-en-clean-architecture)

[🧩 PARTE 8: Inyección de Dependencias](#-parte-8--inyección-de-dependencias)

[🧩 PARTE 9 — MODELO DE TRABAJO](#-parte-9--modelo-de-trabajo)


# Ideas principales (resumen enumerado)

1. Objetivo y principios de Clean Architecture: aislamiento del dominio, dependencia hacia adentro, independencia de frameworks.
2. Fases de migración y enfoque por etapas (alineación, estructura, módulo patrón, replicación).
3. Estructura de proyecto canónica y ejemplo práctico aplicado a `users/members`.
4. Flujo de dependencias: regla sagrada y comprobaciones prácticas.
5. Convenciones de nombrado y sufijos para facilitar lectura y responsabilidades.
6. Reglas de importación entre capas (qué puede y qué no puede importar cada capa).
7. Regla “estructura viva”: no crear carpetas para un solo archivo; cuándo crear carpetas.
8. División semántica de use_cases en `queries` / `mutations` (umbral y motivos).
9. Relación práctica con CQRS: cuándo pensar en migrar y cómo preparar la estructura.
10. Política de nombres y sufijos (reiterado y detallado).
11. Documentación viva: `ARCHITECTURE.md`, `README.md` por módulo, plantilla de módulo patrón.

---

## 🧩 PARTE 1: Desarrollo detallado — Filosofía y estructura

## 1) Objetivo y principios (qué buscamos)

* **Objetivo:** Aislar las reglas de negocio (dominio) del resto (frameworks, DB, infra) para que el núcleo sea independiente, testeable y durable.
* **Principios clave (consejos prácticos):**

  1. **Dominio independiente:** nada del dominio debe importar frameworks (FastAPI, SQLModel).
  2. **Dirección de dependencias:** las dependencias siempre apuntan hacia el dominio.
  3. **Testabilidad:** la lógica de negocio se debe poder probar sin DB ni red.
  4. **Alta cohesión / bajo acoplamiento:** agrupar lo que cambia junto; evitar módulos multi-responsabilidad.
  5. **Arquitectura utilitaria:** la arquitectura sirve al negocio; evitar dogmatismos que compliquen el desarrollo.

---

## 2) Fases de migración (visión práctica)

* **Fase 0 — Alineamiento:** leer y acordar los principios, aceptar convenciones. (1–2 sesiones)
* **Fase 1 — Estructura y convención:** aplicar la estructura canónica en el repo y añadir `ARCHITECTURE.md`.
* **Fase 2 — Módulo patrón (users/members):** migrar completamente este módulo como plantilla.
* **Fase 3 — Replicación:** clonar el patrón en otros módulos (bookings, payments).
* **Fase 4 — Supervisión y ajuste:** automatizar checks (linters/import checks) y refinar convenciones.

> Regla práctica: migruen un módulo completo, revísenlo en equipo y conviértanlo en plantilla antes de migrar el siguiente.

---

## 3) Estructura canónica del proyecto (alto nivel)

Recomiendo la estructura purista pero pragmática:

```
app/
├── domain/
├── application/
├── infrastructure/
├── main.py
└── ARCHITECTURE.md
```

Ahora, **ejemplo concreto para el módulo `users/members`** (modo *módulo patrón* — flat inicial si hay poco contenido, expandible):

```
app/
└── users/                      # Módulo de negocio (bounded context)
    ├── domain/
    │   ├── member.py           # Entidad/agregado (si es único, sin subcarpeta)
    │   ├── exceptions.py       # Excepciones semánticas del dominio
    │   └── value_objects.py
    │
    ├── application/
    │   └── use_cases/
    │       ├── queries/
    │       │   └── get_member_by_id.py
    │       └── mutations/
    │           └── create_member.py
    │
    ├── infrastructure/
    │   ├── db_models.py        # SQLModel <-> mapeos (si sólo uno, no carpeta)
    │   └── repositories.py     # SQLMemberRepositoryImpl
    │
    ├── interfaces/
    │   └── http/
    │       ├── controllers.py  # FastAPI routers para members
    │       └── schemas.py      # Pydantic schemas de entrada/salida
    │
    └── README.md               # Intención del módulo, límites y decisiones
```

**Notas:**

* Si el módulo crece, se transforma `domain/` -> `domain/entities/`, etc. (estructura viva).
* Mantener el módulo autocontenido: todo lo necesario para entender `members` en un vistazo.

---

## 4) Flujo de dependencias — la regla sagrada

* **Definición corta:** las dependencias apuntan hacia adentro (interfaces/puertos en `domain` o `application`, implementaciones en `infrastructure`).
* **Regla práctica:** nunca un archivo en `domain` importa algo de `infrastructure`.
* **Chequeo simple:** en cada PR, revisar imports del módulo modificado; si `domain` importa infra → PR rechazado hasta corregir.
* **Diagrama mental:**

  * FastAPI (interfaces) → Application (use cases) → Domain (entities, repos) ← Infrastructure (adapters)

---

## 5) Convenciones de nombrado y sufijos (para eliminar ambigüedad)

Convenciones uniformes reducen debates sobre dónde poner o cómo llamar algo.

* **Entidades/agregados:** `Member`, `Trainer`, `Plan` (sustantivo singular).
* **Value objects:** `Email`, `Money`, `MembershipType`.
* **Repositorios (interfaces/puertos):** `MemberRepository` (ubicado en domain o application).
* **Repositorios (implementación infra):** `SQLMemberRepository`, `SQLMemberRepositoryImpl` (sufijo `Impl` opcional si no hay ambigüedad).
* **Casos de uso:** `CreateMemberUseCase`, `GetMemberByIdQuery` (si usan CQRS naming).
* **Controllers / Routers:** `MemberController` o `member_router`.
* **Schemas Pydantic:** `MemberIn`, `MemberOut` o `MemberCreate`, `MemberRead`.
* **Exceptions:** `MemberNotFoundError`, `InvalidEmailError`, `RepositoryError`.

> Regla del equipo: escoger **una** convención (p. ej. `SQLMemberRepository`) y usarla consistentemente. No mezclar `Impl` con nombres sin `Impl`.

---

## 6) Reglas de importación entre capas (explicadas)

* **Dominio (`domain/`):** puede importar sólo cosas del dominio puro y tipos estándar. Nunca importar `infrastructure`, `application` ni `interfaces`.
* **Aplicación (`application/`):** puede importar `domain` (entidades, repositorios interfaces) y tipos compartidos; **no** debe importar `infrastructure` directamente (usar inyección de dependencias).
* **Infraestructura (`infrastructure/`):** puede importar `domain` y `application` para implementar adaptadores.
* **Interfaces / HTTP (`interfaces/http`):** puede importar `application` para llamar use cases y `schemas` para validación; no debe contener lógica de negocio.

**Herramientas sugeridas:** configurar checkers en CI (flake8 plugin, isort + script que detecte imports por path) para bloquear imports ilegales.

---

## 7) Regla “estructura viva” — cuándo crear carpetas

* **Regla simple y explícita (adoptar en la guía):**
  **No crear una carpeta para un único archivo** salvo que haya una justificación semántica o crecimiento inminente.
* **Criterios para crear carpeta:**

  1. Hay **≥ 2** archivos del mismo tipo (ej.: varias entidades).
  2. Se espera que en el corto plazo (sprints) ese espacio crezca.
  3. La semántica gana claridad (subdominio suficientemente grande).
* **Ejemplo aplicado:** si sólo existe `member.py`, dejar `domain/member.py`. Cuando aparezca `trainer.py`, crear `domain/entities/` y mover ambos.

---

## 8) División `use_cases` en `queries` y `mutations` (umbral y razones)

* **Cuándo aplicar:** cuando el número de casos de uso supere ~5–6 por módulo o la mezcla lectura/escritura complique la navegación.
* **Beneficios:**

  * Claridad semántica (lectura vs modificación).
  * Facilita introducir patrones como handlers, mediators o CQRS más adelante.
  * Mejora la búsqueda y el onboarding.
* **Estructura recomendada:**

  ```
  application/
  └── use_cases/
      ├── queries/
      └── mutations/
  ```
* **Naming:** `get_member_by_id.py` → query; `create_member.py` → mutation.

---

## 9) Relación con CQRS (práctica, no dogmática)

* **No es obligatorio implementar CQRS**, pero la separación `queries/mutations` facilita una futura migración incremental.
* **Si en el futuro desean CQRS completo:** podrán separar pipelines, handlers y stores de lectura sin romper la intención del dominio.
* **Recomendación:** documentar la intención en `ARCHITECTURE.md` para que cualquiera sepa que la separación es deliberada y preparatoria.

---

## 10) Política de nombres y sufijos (punto 30, consolidado)

* Reafirmación y ejemplos rápidos:

  * `MemberRepository` (interfaz/Protocolo) — `domain`
  * `SQLMemberRepository` o `SQLMemberRepositoryImpl` — `infrastructure`
  * `CreateMemberUseCase` — `application`
  * `member_router` / `MemberController` — `interfaces/http`
  * `MemberIn` / `MemberOut` — `interfaces/http/schemas.py`

**Regla de oro:** un nombre debe indicar claramente la **responsabilidad** del artefacto.

---

## 11) Documentación viva (ARCHITECTURE.md y README por módulo)

* **`ARCHITECTURE.md` (raíz del repo):** incluir:

  * Filosofía y principios acordados.
  * Estructura canónica con ejemplos.
  * Reglas de importación y dependencia.
  * Convenciones de nombrado.
  * Procedimiento para migrar un módulo y checklist de PR.
* **`README.md` por módulo (`app/users/README.md`):** incluir:

  * Intención del módulo (bounded context).
  * Límites: qué contiene / qué no contiene.
  * Plantilla de cómo agregar un nuevo use case/entidad.
  * Lista de excepciones semánticas del módulo.
* **Plantilla de módulo patrón:** generar un `TEMPLATE.md` con estructura mínima para clonar al crear nuevos módulos.

---

## Ejemplo práctico (resumen visual aplicado a `users/members`)

Breve checklist que tu equipo puede usar al crear/editar el módulo `members`:

1. ¿La entidad `Member` vive en `app/users/domain/member.py` y no importa infra? ✅
2. ¿Los repositorios se definen como interfaces en `app/users/domain`? ✅
3. ¿La implementación SQLModel está en `app/users/infrastructure/repositories.py`? ✅
4. ¿Los use cases están en `app/users/application/use_cases/{queries,mutations}`? ✅
5. ¿El router FastAPI está en `app/users/interfaces/http/controllers.py` y sólo llama use cases via DI? ✅
6. ¿Existe `app/users/README.md` con límites e intención? ✅

---

## Reglas prácticas para que no haya ambigüedad en el equipo (resumen)

1. Las dependencias apuntan hacia el dominio; bloquear imports contrarios en CI.
2. No crear carpetas para 1 archivo (salvo justificación documentada).
3. Dividir `use_cases` en `queries` / `mutations` si > 5–6 casos de uso.
4. Nombrado uniforme y sufijos claros (`Repository`, `SQL...`, `UseCase`, `Router`).
5. `ARCHITECTURE.md` obligatorio y `README.md` por módulo.
6. Convertir el módulo `users/members` en plantilla antes de migrar otros.

---

## 🧩 PARTE 2: CAPA DE DOMINIO

### 1. **Propósito de la capa de dominio**

La capa de dominio representa el **modelo del negocio puro**, completamente **independiente de frameworks, bases de datos o detalles técnicos**.
Debe poder ejecutarse sin necesidad de FastAPI, SQLModel ni ningún otro componente externo.

El dominio es el **lenguaje del negocio expresado en código**.
Su objetivo es que cualquiera del equipo (devs, product manager o incluso el dueño del gimnasio) pueda entender cómo funciona el negocio **leyendo el código del dominio**.

---

### 2. **Estructura de carpetas recomendada**

Para el módulo `usuarios` (o `members`, si lo prefieren en inglés):

```
/gym_app
 └── domain/
      └── members/
           ├── __init__.py
           ├── member.py             # Entidad principal o agregado raíz
           ├── value_objects.py      # Objetos de valor (si son pocos)
           ├── services.py           # Servicios de dominio (opcional)
           ├── exceptions.py         # Excepciones del dominio
           └── interfaces.py         # Contratos abstractos (si aplica)
```

🔹 **Nota importante:**
Si el módulo tiene una sola entidad (por ejemplo, `Member`), **no es necesario crear subcarpetas** como `entities/` o `value_objects/`.
La simplicidad también es un valor arquitectónico.
Solo se crean subcarpetas cuando hay **varias entidades o demasiados value objects** (más de 4–5).

---

### 3. **Entidades y agregados**

**Conceptos clave:**

* Una **Entidad** es un objeto con identidad propia (por ejemplo, un `Member` o `Trainer`).
* Un **Agregado** es una entidad que actúa como **raíz** y **coordina la consistencia** del resto de objetos relacionados.

**Reglas prácticas:**

1. Toda entidad debe tener un **identificador único** (`id`) y un **comportamiento relevante**.
2. Si una entidad depende conceptualmente de otra (por ejemplo, `Membership` depende de `Member`), debe gestionarse **a través del agregado raíz**.
3. No expongas entidades hijas fuera del agregado.
   Cualquier modificación debe pasar por la raíz (`Member` actualiza su `Membership`).
4. Usa métodos de instancia o de clase para expresar **invariantes**.
   Ejemplo: un `Member` no puede estar activo si su `Membership` ha expirado.

**Ejemplo simplificado (`member.py`):**

```python
from datetime import date
from typing import Optional
from .value_objects import Email
from .exceptions import MembershipExpiredError

class Member:
    def __init__(self, id: int, name: str, email: Email, membership_expiration: Optional[date]):
        self.id = id
        self.name = name
        self.email = email
        self.membership_expiration = membership_expiration

    def is_active(self) -> bool:
        return self.membership_expiration is not None and self.membership_expiration >= date.today()

    def ensure_is_active(self):
        if not self.is_active():
            raise MembershipExpiredError(f"El miembro {self.name} tiene la membresía expirada.")
```

---

### 4. **Objetos de valor (Value Objects)**

Los **Value Objects** representan conceptos **sin identidad**, definidos solo por sus atributos y reglas.
Por ejemplo: `Email`, `PhoneNumber`, `Money`, `Weight`.

**Características:**

* Son **inmutables**.
* Validan sus propios datos en `__post_init__` (si se usa `@dataclass` o `pydantic.BaseModel`).
* Encapsulan lógica semántica (por ejemplo, validación de formato de correo o peso mínimo permitido).

**Ejemplo (`value_objects.py`):**

```python
from dataclasses import dataclass
import re
from .exceptions import InvalidEmailError

@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.value):
            raise InvalidEmailError(f"El correo '{self.value}' no tiene un formato válido.")
```

---

### 5. **Servicios de dominio**

Los **servicios de dominio** encapsulan operaciones del negocio que:

* **No pertenecen naturalmente** a una entidad o value object.
* **Requieren coordinación** entre múltiples entidades/agregados.

Ejemplo: calcular la renovación automática de membresías, o transferir créditos entre dos usuarios.

**Ejemplo (`services.py`):**

```python
from datetime import date, timedelta
from .exceptions import MembershipExpiredError

def renew_membership(member, days: int):
    if not member.is_active():
        raise MembershipExpiredError(f"No se puede renovar una membresía expirada para {member.name}.")
    member.membership_expiration = date.today() + timedelta(days=days)
```

**Nota:**
No siempre se necesita un archivo `services.py`.
Si solo hay uno o dos métodos de dominio, es mejor mantenerlos dentro de la entidad raíz (`Member`).

---

### 6. **Excepciones del dominio**

Cada módulo de dominio debe tener sus **propias excepciones semánticas**.
Por ejemplo:

```python
class InvalidEmailError(ValueError):
    """El correo electrónico no cumple con el formato esperado."""

class MembershipExpiredError(ValueError):
    """La membresía del usuario ha expirado."""
```

Esto permite:

* Aislar los errores del dominio.
* Mantener el flujo de control claro.
* Mejorar la trazabilidad y el testing.

---

### 7. **Independencia tecnológica**

El dominio **no puede importar nada** de:

* `fastapi`
* `sqlmodel`
* `pydantic`
* `infrastructure`
* `application`

Solo debe depender de:

* `typing`, `datetime`, `dataclasses`, `uuid`, `abc`
* Módulos del mismo dominio

---

### 8. **Reglas prácticas de diseño**

1. Mantén el dominio **sin dependencias externas**.
2. Los métodos deben tener **nombres expresivos** (en lenguaje del negocio).
3. Evita duplicar lógica en entidades y servicios: cada comportamiento debe tener un solo responsable.
4. Las validaciones estructurales van en **Value Objects**, las de negocio en **Entidades o Servicios de Dominio**.
5. Usa **excepciones**, no retornos silenciosos (`None` o `False`), para violaciones de invariantes.
   Los retornos nulos solo se usan para operaciones no críticas o consultas.

---

## ⚙️ PARTE 3: CAPA DE APLICACIÓN

### 1. **Propósito de la capa de aplicación**

La capa de aplicación **usa el dominio para ejecutar acciones concretas** (casos de uso), como:

* Registrar un nuevo miembro
* Renovar una membresía
* Consultar la información de un miembro
* Eliminar o suspender un usuario

A diferencia del dominio (que **modela reglas del negocio**), la capa de aplicación **coordina el flujo**:

* Orquesta entidades y servicios del dominio.
* Llama a los repositorios abstractos para obtener o guardar datos.
* Controla transacciones y flujos de error.
* No contiene lógica del negocio, solo **usa la del dominio**.

---

### 2. **Estructura de carpetas recomendada**

Usando el módulo `members` como ejemplo:

```
/gym_app
 └── application/
      └── members/
           ├── __init__.py
           ├── use_cases/
           │    ├── __init__.py
           │    ├── register_member.py
           │    ├── renew_membership.py
           │    ├── get_member_info.py
           │    └── deactivate_member.py
           ├── dtos.py
           ├── interfaces.py
           ├── exceptions.py
           └── events.py
```

🔹 **Regla práctica:**
Cuando haya más de **6 casos de uso**, puedes dividir `use_cases/` en:

```
use_cases/
 ├── queries/
 └── mutations/
```

Esto sigue el principio **CQRS** (Command Query Responsibility Segregation):

* `queries/`: casos de uso que **no modifican el estado** (consultas).
* `mutations/`: casos de uso que **modifican el estado** (acciones).

---

### 3. **Caso de uso: estructura base**

Cada caso de uso debe ser una **clase o callable** con un único propósito.
Debe depender de **interfaces abstractas**, no de implementaciones concretas.

Ejemplo (`register_member.py`):

```python
from datetime import date, timedelta
from gym_app.domain.members.member import Member
from gym_app.domain.members.value_objects import Email
from gym_app.domain.members.exceptions import InvalidEmailError
from gym_app.application.members.interfaces import MemberRepository

class RegisterMember:
    def __init__(self, member_repo: MemberRepository):
        self.member_repo = member_repo

    async def execute(self, name: str, email: str, duration_days: int = 30):
        try:
            member_email = Email(email)
        except InvalidEmailError as e:
            raise ValueError(f"Error al registrar miembro: {str(e)}")

        member = Member(
            id=None,
            name=name,
            email=member_email,
            membership_expiration=date.today() + timedelta(days=duration_days)
        )

        await self.member_repo.add(member)
        return member
```

---

### 4. **Interfaces (puertos de entrada/salida)**

La capa de aplicación **define contratos**, no implementaciones.

Ejemplo (`interfaces.py`):

```python
from abc import ABC, abstractmethod
from typing import Optional
from gym_app.domain.members.member import Member

class MemberRepository(ABC):
    @abstractmethod
    async def add(self, member: Member) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, member_id: int) -> Optional[Member]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[Member]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, member: Member) -> None:
        raise NotImplementedError
```

Estas interfaces luego serán **implementadas en la capa de infraestructura**, por ejemplo con SQLModel.

---

### 5. **DTOs (Data Transfer Objects)**

Los DTOs encapsulan los datos de entrada/salida entre capas, evitando exponer directamente las entidades del dominio.

Ejemplo (`dtos.py`):

```python
from pydantic import BaseModel, EmailStr
from datetime import date

class RegisterMemberDTO(BaseModel):
    name: str
    email: EmailStr
    duration_days: int = 30

class MemberResponseDTO(BaseModel):
    id: int
    name: str
    email: str
    membership_expiration: date
    is_active: bool
```

💡 *Nota:* Aunque Pydantic es un framework externo, **su uso aquí es válido** porque la capa de aplicación **sí puede depender de frameworks**, siempre que no invadan el dominio.

---

### 6. **Eventos de DOMINIO**

Los eventos en esta capa reflejan **acciones relevantes para el negocio** que pueden interesar a otras partes del sistema. Son declarados en la capa de DOMINIO*

Ejemplo (`events.py`):

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class MemberRegisteredEvent:
    member_id: int
    occurred_on: datetime
```

Estos eventos pueden ser publicados, por ejemplo, para enviar un correo de bienvenida o actualizar métricas.
(Podrías usar un *Event Bus* inyectado por dependencia).

La publicacion de eventos se puede hacer desde Application

Igual que para los handlers de los eventos deben ir en Application

---

### 7. **Errores y excepciones de aplicación**

Las excepciones aquí **no son de negocio**, sino de **flujo de aplicación** (repositorios, validaciones, permisos, etc.).

Ejemplo (`exceptions.py`):

```python
class MemberAlreadyExistsError(Exception):
    """Se intentó registrar un miembro que ya existe."""

class MemberNotFoundError(Exception):
    """No se encontró el miembro solicitado."""
```

🔹 **Cuándo usar excepciones vs valores nulos:**

* **Excepciones:** para errores que rompen el flujo normal (por ejemplo, duplicados, fallos de persistencia, permisos).
* **Retornar None:** para resultados esperables, como “no se encontró el miembro” en una búsqueda simple.

---

### 8. **Reglas y buenas prácticas**

1. **Un caso de uso = una acción del negocio.**
2. No mezclar lógica de negocio aquí, solo **usar el dominio**.
3. Los casos de uso **no deben importar de infraestructura ni controladores**.
4. Todo acceso a datos debe pasar por **repositorios abstractos**.
5. Si un caso de uso requiere transacciones, que sea gestionado aquí (no en la API).
6. Manejar los errores de dominio dentro del caso de uso, lanzando excepciones de aplicación cuando sea apropiado.
7. Mantén los casos de uso **fáciles de testear unitariamente** (mockeando dependencias).

---

### 9. **Ejemplo completo de flujo**

1. El controlador (`FastAPI endpoint`) recibe la solicitud.
2. Valida la entrada con un DTO (`RegisterMemberDTO`).
3. Inyecta el caso de uso `RegisterMember`.
4. El caso de uso crea un `Member` del dominio.
5. Llama al `MemberRepository` para persistirlo.
6. Devuelve un `MemberResponseDTO` al controlador.

Este flujo garantiza:

* **Aislamiento** del dominio.
* **Reutilización** de los casos de uso (por ejemplo, en tareas de background o eventos).
* **Testabilidad** y claridad en la intención del código.

---

## 🧱 PARTE 4: CAPA DE INFRAESTRUCTURA

### 1. **Propósito general**

La capa de infraestructura contiene todas las implementaciones **detalladas** de las interfaces definidas en la capa de aplicación y dominio.

Su objetivo es:

* Concretar **repositorios**, **adapters**, **event bus**, **proveedores de servicios externos**, etc.
* Definir cómo los datos **persisten o viajan** fuera del dominio.
* **Nunca** contener lógica de negocio.
* Ser totalmente **reemplazable o testeable** (por mocks, por ejemplo).

---

### 2. **Estructura de carpetas recomendada**

Usando el módulo `members` como ejemplo:

```
/gym_app
 └── infrastructure/
      ├── __init__.py
      ├── db/
      │    ├── __init__.py
      │    ├── base.py
      │    └── session.py
      ├── members/
      │    ├── __init__.py
      │    ├── models.py
      │    ├── repositories.py
      │    ├── mappers.py
      │    └── di.py
      ├── event_bus/
      │    ├── __init__.py
      │    └── simple_event_bus.py
      └── config.py
```

---

### 3. **Base de datos y SQLModel**

#### `base.py`

Aquí centralizamos la configuración de los metadatos base para todas las tablas.

```python
from sqlmodel import SQLModel

# Base común para todas las entidades de la base de datos
class Base(SQLModel):
    pass
```

#### `session.py`

Aquí configuramos la conexión y el `sessionmaker`.

```python
from sqlmodel import Session, create_engine
from contextlib import contextmanager
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./gym_app.db")
engine = create_engine(DATABASE_URL, echo=True)

@contextmanager
def get_session():
    with Session(engine) as session:
        yield session
```

💡 *Nota:*
En proyectos grandes, el `engine` se inyecta mediante `Dependency Injection` para mantener la independencia del entorno (tests, dev, prod).

---

### 4. **Modelo de infraestructura (ORM model)**

El modelo SQLModel **no es una entidad de dominio**.
Es una representación **de persistencia**, que puede tener campos adicionales o adaptados.

#### `models.py`

```python
from sqlmodel import SQLModel, Field
from datetime import date

class MemberTable(SQLModel, table=True):
    __tablename__ = "members"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    membership_expiration: date
    is_active: bool = True
```

---

### 5. **Mapper (infraestructura ↔ dominio)**

Los mappers permiten traducir entre la entidad del dominio (`Member`) y la tabla de persistencia (`MemberTable`).

**Esto tambien podria ser en el propio repositorio de la entidad**

#### `mappers.py`

```python
from gym_app.domain.members.member import Member
from gym_app.domain.members.value_objects import Email
from .models import MemberTable

def to_domain(entity: MemberTable) -> Member:
    return Member(
        id=entity.id,
        name=entity.name,
        email=Email(entity.email),
        membership_expiration=entity.membership_expiration,
        is_active=entity.is_active
    )

def to_table(entity: Member) -> MemberTable:
    return MemberTable(
        id=entity.id,
        name=entity.name,
        email=entity.email.value,
        membership_expiration=entity.membership_expiration,
        is_active=entity.is_active
    )
```

---

### 6. **Repositorio (implementación concreta)**

Aquí se implementan las interfaces del repositorio definidas en `application.members.interfaces` o tambien puede ser en `domain/interfaces`.

Para evitar el repetir la session se puede pasar por inyeccion de dependencias

#### `repositories.py`

```python
from typing import Optional
from sqlmodel import select
from gym_app.domain.members.member import Member
from gym_app.application.members.interfaces import MemberRepository
from gym_app.infrastructure.db.session import get_session
from gym_app.infrastructure.members.models import MemberTable
from gym_app.infrastructure.members.mappers import to_domain, to_table

class MemberRepositoryImpl(MemberRepository):

    async def add(self, member: Member) -> None:
        member_row = to_table(member)
        with get_session() as session:
            session.add(member_row)
            session.commit()
            session.refresh(member_row)
        member.id = member_row.id

    async def get_by_id(self, member_id: int) -> Optional[Member]:
        with get_session() as session:
            result = session.exec(select(MemberTable).where(MemberTable.id == member_id)).first()
            return to_domain(result) if result else None

    async def get_by_email(self, email: str) -> Optional[Member]:
        with get_session() as session:
            result = session.exec(select(MemberTable).where(MemberTable.email == email)).first()
            return to_domain(result) if result else None

    async def update(self, member: Member) -> None:
        with get_session() as session:
            existing = session.get(MemberTable, member.id)
            if not existing:
                raise ValueError(f"Miembro con ID {member.id} no encontrado")
            updated = to_table(member)
            session.merge(updated)
            session.commit()
```

---

### 7. **Inyección de dependencias (Dependency Injection)**

Usaremos la librería [`dependency-injector`](https://python-dependency-injector.ets-labs.org/)
(la más estable para proyectos productivos).

#### `di.py`

```python
from dependency_injector import containers, providers
from gym_app.infrastructure.members.repositories import MemberRepositoryImpl

class MemberContainer(containers.DeclarativeContainer):
    """Contenedor de dependencias para el módulo Members"""

    member_repository = providers.Factory(MemberRepositoryImpl)
```

Y luego, en la capa de **interfaces (controladores)** o **main**, se puede hacer el *wiring*:

```python
from gym_app.infrastructure.members.di import MemberContainer
from gym_app.application.members.use_cases.register_member import RegisterMember

container = MemberContainer()
register_member_use_case = RegisterMember(container.member_repository())
```

De este modo:

* El caso de uso no sabe **cómo** se crea el repositorio.
* Todo queda **inyectado** y desacoplado.

---

### 8. **Eventos y buses de infraestructura**

Un ejemplo simple de event bus puede ser un *publisher/subscriber* interno.

#### `simple_event_bus.py`

```python
from typing import Callable, Dict, List, Type

class SimpleEventBus:
    def __init__(self):
        self.subscribers: Dict[Type, List[Callable]] = {}

    def subscribe(self, event_type: Type, handler: Callable):
        self.subscribers.setdefault(event_type, []).append(handler)

    async def publish(self, event):
        handlers = self.subscribers.get(type(event), [])
        for handler in handlers:
            await handler(event)
```

Esto se puede inyectar igual que los repositorios, manteniendo el dominio aislado de la infraestructura.

---

### 9. **Buenas prácticas y convenciones**

1. **Nunca importar la infraestructura desde el dominio o aplicación.**
2. **Mantén los mappers explícitos**, no automáticos, para evitar acoplamiento implícito.
3. Evita usar `SQLModel` directamente en los casos de uso: **usa repositorios abstractos.**
4. Usa `Dependency Injection` para orquestar repositorios, event bus, cache, etc.
5. La capa de infraestructura **puede depender** de frameworks, ORM, etc.
   Pero sus efectos deben **terminar en interfaces abstractas** de la capa de aplicación.
6. Es recomendable **una carpeta por módulo funcional** (ej. `members`, `payments`, `trainers`).
7. Todos los *containers* deben tener un prefijo coherente (`MembersContainer`, `PaymentsContainer`), y luego agregarse a un contenedor raíz global.

---

### 10. **Flujo completo de ejemplo**

1. El `controller` (FastAPI) recibe el request.
2. Inyecta `RegisterMember`, con `MemberRepositoryImpl` desde el contenedor.
3. El caso de uso crea un `Member` (entidad de dominio).
4. El `MemberRepositoryImpl` guarda el `MemberTable` en SQLModel.
5. Se publica un `MemberRegisteredEvent`.
6. El controlador devuelve el DTO de respuesta.

---

## 🧩 PARTE 5: Estructura base del módulo `interfaces`

```
app/
├── interfaces/
│   ├── controllers/
│   │   └── member_controller.py
│   ├── errors/
│   │   ├── http_error_handler.py
│   │   └── application_exceptions.py
│   └── __init__.py
```
---

## 🎯 Objetivo de esta capa

1. Exponer los **casos de uso** como **endpoints HTTP**.
2. Convertir las **entradas HTTP (Request)** en **DTOs** de aplicación.
3. Invocar los **use cases** del dominio mediante **inyección de dependencias**.
4. Traducir las **excepciones o errores de negocio** en **respuestas HTTP estandarizadas**.
5. Mantener la **capa de presentación desacoplada** del dominio y la infraestructura.

---

## ⚙️ 2. Dependency Injection con `dependency_injector`

Instalamos el paquete oficial:

```bash
pip install dependency-injector
```

Lo usaremos para declarar un **contenedor de dependencias** más profesional que el “manual” que usamos antes.

---

## 📦 3. Configuración del contenedor (`container.py`)

Actualizamos el contenedor anterior para usar `dependency_injector`:

La inyeccion de dependencias no tiene que hacerse en infraestructura, no tiene por que ser en Application, Domain tampoco, ya que es como el pegamento que une las capas

```python
# app/infrastructure/di/container.py
from dependency_injector import containers, providers

from app.infrastructure.database.repositories.member_repository_sqlmodel import MemberRepositorySQLModel
from app.application.use_cases.register_member import RegisterMemberUseCase

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["app.interfaces.controllers.member_controller"]
    )

    # Proveedores de infraestructura
    member_repository = providers.Factory(MemberRepositorySQLModel)

    # Casos de uso
    register_member_use_case = providers.Factory(
        RegisterMemberUseCase,
        member_repository=member_repository
    )
```

🧠 **Notas:**

* `wiring_config` permite a `dependency_injector` “inyectar” dependencias directamente en los controladores.
* `providers.Factory()` crea una instancia nueva cada vez; podrías usar `Singleton()` para servicios globales.

---

## 🧱 4. Manejo de excepciones, mapeo de excepciones y demas usando Exception Handlers de FastApi)

La idea es mantener **los errores del dominio limpios y semánticos**.

```python
# app/interfaces/errors/application_exceptions.py
class ApplicationError(Exception):
    """Error base para la capa de aplicación."""

class MemberAlreadyExistsError(ApplicationError):
    """Se lanza cuando se intenta registrar un miembro ya existente."""
```

---

Yo pienso que podriamos tener solo el Handler respectivo e importar las excepciones y ahi personalizar, no es necesario este application_exceptions aqui, las excepciones de application van en la propia capa de Application

## 🚨 5. Mapeo de errores a HTTP (`http_error_handler.py`)

Creamos un **middleware** o función auxiliar para traducir estos errores en respuestas HTTP estándar.

```python
# app/interfaces/errors/http_error_handler.py
from fastapi.responses import JSONResponse
from fastapi import Request
from app.interfaces.errors.application_exceptions import MemberAlreadyExistsError

async def http_error_handler(request: Request, exc: Exception):
    if isinstance(exc, MemberAlreadyExistsError):
        return JSONResponse(
            status_code=409,
            content={"detail": "El miembro ya está registrado."}
        )
    elif isinstance(exc, ValueError):
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)}
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"detail": "Error interno del servidor."}
        )
```
Puede ser un middleware, pero https://fastapi.tiangolo.com/tutorial/handling-errors/#install-custom-exception-handlers puede ser usar @app.exception.handler
---

## 🧭 6. Controlador de miembros (`member_controller.py`)

Aquí ocurre la magia: el **caso de uso se inyecta automáticamente** por `dependency_injector`.
Este archivo representa la frontera entre FastAPI y la aplicación.

```python
# app/interfaces/controllers/member_controller.py
from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from app.application.dto.member_dto import MemberDTO
from app.application.use_cases.register_member import RegisterMemberUseCase
from app.infrastructure.di.container import Container
from app.interfaces.errors.application_exceptions import MemberAlreadyExistsError

router = APIRouter(prefix="/members", tags=["Members"])

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Miembro registrado exitosamente"},
        409: {"description": "El miembro ya existe"},
        400: {"description": "Error de validación"},
        500: {"description": "Error interno del servidor"},
    },
)
@inject
def register_member(
    dto: MemberDTO,
    use_case: RegisterMemberUseCase = Depends(Provide[Container.register_member_use_case])
):
    try:
        member = use_case.execute(dto)
        return {"id": member.id, "name": member.name, "email": member.email}
    except MemberAlreadyExistsError as e:
        raise e  # Será interceptado por el manejador HTTP
```

🧠 **Claves del wiring real:**

* `@inject` habilita la inyección automática.
* `Provide[Container.register_member_use_case]` obtiene el caso de uso desde el contenedor.
* El controlador no instancia nada directamente → 100 % **desacoplado**.

---

## 🧩 7. Integración en `main.py`

Conectamos todo: FastAPI + contenedor + manejador de errores.

```python
# app/main.py
from fastapi import FastAPI
from app.infrastructure.database.connection import init_db
from app.interfaces.controllers import member_controller
from app.infrastructure.di.container import Container
from app.interfaces.errors.http_error_handler import http_error_handler
from app.interfaces.errors.application_exceptions import ApplicationError

def create_app() -> FastAPI:
    container = Container()
    app = FastAPI(title="Clean Architecture Example")
    app.container = container  # Asocia el contenedor a la app

    init_db()

    app.include_router(member_controller.router)
    app.add_exception_handler(ApplicationError, http_error_handler)

    return app

app = create_app()
```

---

## 🧠 8. Flujo completo (resumen)

1. El cliente envía un `POST /members` con los datos.
2. FastAPI convierte el body a `MemberDTO`.
3. `dependency_injector` inyecta el `RegisterMemberUseCase`.
4. El caso de uso ejecuta la lógica (validaciones, dominio, repositorio).
5. Si algo falla, lanza un `ApplicationError`.
6. El manejador global convierte la excepción en una respuesta HTTP clara.

---

## ✅ 9. Ventajas de este enfoque

| Aspecto                    | Beneficio                                                                              |
| -------------------------- | -------------------------------------------------------------------------------------- |
| **Desacoplamiento total**  | Ningún controlador conoce detalles del ORM ni de la infraestructura.                   |
| **Testabilidad**           | Puedes testear los controladores y casos de uso inyectando dependencias falsas.        |
| **Escalabilidad**          | Cambiar de SQLModel a PostgreSQL, Redis o una API externa no afecta los controladores. |
| **Uniformidad de errores** | Todos los fallos siguen un formato HTTP predecible.                                    |
| **Inyección declarativa**  | Evita tener que pasar dependencias manualmente.                                        |

---

## 🚀 Ejemplo de prueba rápida con `curl`

```bash
curl -X POST http://127.0.0.1:8000/members \
     -H "Content-Type: application/json" \
     -d '{"name": "Marcos", "email": "marcos@example.com"}'
```

* ✅ Si todo va bien → `201 Created`
* ⚠️ Si el correo ya existe → `409 Conflict`
* ❌ Si hay error interno → `500 Internal Server Error`

---
Perfecto, Marcos 👌
Entramos a una de las partes **más decisivas para la consistencia y mantenibilidad** de una arquitectura limpia:
la **gestión semántica y unificada de errores**.
Aquí es donde un código robusto se diferencia de uno simplemente “que funciona”.

---


# 🧩 PARTE 6: Testing en Clean Architecture

---

## 🎯 Objetivos

1. **Probar el dominio** sin depender de infraestructura.
2. **Testear casos de uso (application)** con repositorios simulados.
3. **Testear controladores (interfaces)** con FastAPI TestClient y un contenedor configurado para pruebas.
4. Asegurar una **pirámide de tests equilibrada**: más tests de unidad, menos de integración.

---

## ⚖️ 1. Filosofía general de testing en Clean Architecture

1. **Dominio:** Tests puros, sin mocks ni bases de datos.

   * Se validan reglas de negocio y consistencia de entidades.

2. **Aplicación:** Tests con *repositorios falsos* o *mocks*.

   * Se valida el flujo del caso de uso.

3. **Infraestructura:** Tests de integración reales con la DB (opcional).

   * Se valida la correcta persistencia.

4. **Interfaces (controladores):** Tests end-to-end o de API.

   * Se asegura que el wiring y la conversión de errores funcionen.

> 📏 “Mientras más cerca del dominio esté el test, más rápido y confiable será”.

---

## 🧱 2. Estructura del directorio de tests

```
tests/
│
├── domain/
│   ├── test_value_objects.py
│   └── test_entities.py
│
├── application/
│   ├── test_use_case_create_member.py
│   └── test_use_case_get_member.py
│
├── infrastructure/
│   ├── test_repo_member_sqlmodel.py
│   └── containers_test.py
│
└── interfaces/
    └── test_api_members.py

```

Cada carpeta refleja una capa de la arquitectura, preservando el principio de independencia entre capas.

---

## 🧪 3. Test del dominio (unitario puro)

Ejemplo: validar reglas en `Member` (sin DB ni FastAPI).

```python
# tests/domain/test_member_entity.py
import pytest
from app.domain.members.entities.member import Member

def test_member_creation():
    member = Member(id=1, name="Marcos", email="marcos@example.com")
    assert member.name == "Marcos"
    assert member.email == "marcos@example.com"

def test_member_invalid_email():
    with pytest.raises(ValueError):
        Member(id=1, name="Test", email="not-an-email")
```

> 🔹 Aquí se prueban las **invariantes** del dominio (reglas que siempre deben cumplirse).

>💡 Nota:
> Los Value Objects deben lanzar excepciones semánticas, como InvalidEmailError, para facilitar el manejo en capas superiores.

---

## 🧰 4. Test de casos de uso (application layer)

Probaremos `RegisterMemberUseCase` usando un *repositorio falso* (mock o stub).
Aquí probamos la lógica de coordinación.
Se usan fakes o repositorios en memoria, nunca la base de datos real.

```python
# tests/application/test_register_member_use_case.py
import pytest
from app.application.use_cases.register_member import RegisterMemberUseCase
from app.domain.members.entities.member import Member
from app.interfaces.errors.application_exceptions import MemberAlreadyExistsError

class FakeMemberRepository:
    def __init__(self):
        self.members = {}

    def get_by_email(self, email):
        return self.members.get(email)

    def save(self, member: Member):
        self.members[member.email] = member
        return member

def test_register_member_success():
    repo = FakeMemberRepository()
    use_case = RegisterMemberUseCase(member_repository=repo)
    dto = {"name": "Marcos", "email": "marcos@example.com"}
    member = use_case.execute(dto)
    assert member.email == "marcos@example.com"

def test_register_member_already_exists():
    repo = FakeMemberRepository()
    use_case = RegisterMemberUseCase(member_repository=repo)
    existing = Member(id=1, name="Marcos", email="marcos@example.com")
    repo.save(existing)
    dto = {"name": "Marcos", "email": "marcos@example.com"}
    with pytest.raises(MemberAlreadyExistsError):
        use_case.execute(dto)
```

> ✅ Aquí validamos la **lógica del flujo de aplicación**, sin tocar la base de datos ni FastAPI.

---

## 🧱 5. Test de infraestructura (repositorio real con SQLModel)

Aquí sí interactuamos con la DB (SQLite en memoria).

```python
# tests/infrastructure/test_member_repository_sqlmodel.py
import pytest
from sqlmodel import SQLModel, Session, create_engine
from app.infrastructure.database.repositories.member_repository_sqlmodel import MemberRepositorySQLModel
from app.domain.members.entities.member import Member

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_save_and_get_member(session):
    repo = MemberRepositorySQLModel(session=session)
    member = Member(id=None, name="Marcos", email="marcos@example.com")
    repo.save(member)
    found = repo.get_by_email("marcos@example.com")
    assert found.email == "marcos@example.com"
```

> ⚙️ Este tipo de tests son **más lentos** y deben limitarse a lo esencial. Se ejecuta con la base de datos temporal y confirma que el mapping ORM está correcto.

---

## 🌐 6. Test de controladores (FastAPI + Dependency Injector)

Estos tests validan que:

* El wiring funcione correctamente.
* El flujo HTTP → caso de uso → respuesta esté alineado.
* Los errores se transformen en respuestas adecuadas.

```python
# tests/interfaces/test_member_controller.py
import pytest
from fastapi.testclient import TestClient
from app.main import create_app

@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)

def test_register_member_success(client):
    response = client.post(
        "/members/",
        json={"name": "Marcos", "email": "marcos@example.com"},
    )
    assert response.status_code == 201
    assert "id" in response.json()

def test_register_member_conflict(client):
    client.post("/members/", json={"name": "Marcos", "email": "marcos@example.com"})
    response = client.post("/members/", json={"name": "Marcos", "email": "marcos@example.com"})
    assert response.status_code == 409
    assert response.json()["detail"] == "El miembro ya está registrado."
```

> 💡 Aquí se testea el **comportamiento observable del sistema**, no los detalles internos. Este test usa el wiring real del contenedor, simulando una petición real.

---

## 🧩 7. Configuración de `pytest` (`conftest.py`)

Puedes definir aquí tu configuración global de fixtures o variables de entorno para aislar la DB o el contenedor.

```python
# tests/conftest.py
import pytest
from app.infrastructure.di.container import Container

@pytest.fixture(autouse=True)
def override_container(monkeypatch):
    """Fixture que evita usar dependencias reales durante los tests."""
    container = Container()
    monkeypatch.setattr("app.main.Container", lambda: container)
```

---

## 📊 8. Pirámide ideal de tests en Clean Architecture

```
             (más rápidos, más confiables)
       ┌───────────────────────────────┐
       │       Dominio (70%)           │  ← sin mocks
       ├───────────────────────────────┤
       │     Aplicación (20%)          │  ← repos falsos / mocks
       ├───────────────────────────────┤
       │     Infraestructura (5%)      │  ← DB real
       ├───────────────────────────────┤
       │     Interfaces / E2E (5%)     │  ← HTTP real
       └───────────────────────────────┘
```

> Cada capa se testea **en aislamiento**, y solo las capas externas prueban la integración completa.

---
## 🧠 9. Política de uso de Mocks y Fakes
Tipo de prueba	Recurso simulado	Herramienta recomendada
Dominio	Ninguno	-
Aplicación	Fake repositorios	Clases in-memory
Infraestructura	DB temporal	SQLite in-memory
Interfaces	Ninguno	TestClient real

Mocks → solo cuando se quiere verificar interacciones.
Fakes → para simular comportamiento real de infraestructura.

## 🪶 10. Convenciones de nomenclatura
Capa	Prefijo sugerido	Ejemplo
Dominio	test_domain_	test_domain_value_objects.py
Aplicación	test_use_case_	test_use_case_create_member.py
Infraestructura	test_repo_	test_repo_member_sqlmodel.py
Interfaces	test_api_	test_api_members.py
📊 6.9 Cobertura y calidad
Herramienta recomendada:
pytest --cov=gym_app --cov-report=term-missing

Estándares del equipo:

Cobertura mínima: 85%

Tiempos de ejecución: < 2s por test unitario

Tests de integración: separados en pipelines lentos

## 💡 11. Recomendaciones finales

Usa pytest.mark.asyncio siempre que haya async/await.

Evita el orden dependiente entre tests (cada uno crea sus propios datos).

Define fixtures compartidos para datos comunes (member_data, fake_repo, etc.).

Integra el pipeline de tests en CI/CD.

Revisa cobertura al menos una vez por sprint.

---

## ✅ 12. Recomendaciones prácticas

1. **Evita mocks innecesarios** en el dominio; usa objetos reales.
2. **Usa repos falsos o en memoria** para testear casos de uso.
3. **Configura tests paralelos** con `pytest-xdist` si el proyecto crece.
4. **Nombra tus tests por intención**, no por implementación (`test_register_member_conflict`, no `test_post_member_conflict`).
5. **Automatiza los tests** en CI (GitHub Actions, GitLab CI o Jenkins).

---

## 🧾 Resumen final de la Parte 6

| Nivel               | Propósito                           | Ejemplo               |
| ------------------- | ----------------------------------- | --------------------- |
| **Dominio**         | Validar reglas de negocio puras     | `Email`, `Member`     |
| **Aplicación**      | Coordinar entidades y repositorios  | `CreateMemberUseCase` |
| **Infraestructura** | Validar persistencia y mappings     | `MemberSQLRepository` |
| **Interfaces**      | Validar endpoints y respuestas HTTP | `/members/` API       |


Testing en Clean Architecture no se trata solo de “cubrir código”, sino de **proteger los límites entre capas**.
Cada test debe comprobar que las dependencias **no se filtren** y que las reglas del dominio se mantengan inmutables.

---

## ⚙️ PARTE 7: Creación y Manejo de Excepciones Semánticas en Clean Architecture

---

## 🎯 Objetivos

1. Crear una **jerarquía coherente de excepciones** entre capas.
2. Definir **cuándo lanzar** una excepción y cuándo devolver `None` o `False`.
3. Estandarizar el **manejo y conversión a errores HTTP** (FastAPI).
4. Incorporar **patrones de diseño para errores**:

   * `Error Object Pattern`
   * `Application Error Codes`
   * `Result/Either Pattern`

Todo esto bajo el módulo `members` como ejemplo base.

---

## 🧱 1. Filosofía general

Las excepciones deben **tener intención semántica**, no técnica.

* ❌ **Malo:** `raise ValueError("Email inválido")`
* ✅ **Bueno:** `raise InvalidEmailError(email)`

El propósito es que al leer el nombre de la excepción,
puedas **entender el problema sin mirar el mensaje**.

---

## 🧩 2. Jerarquía base de excepciones

Una estructura clara evita el caos de `ValueError` o `Exception` genéricos.

```
app/
└── interfaces/
    └── errors/
        ├── base_exceptions.py
        ├── domain_exceptions.py
        ├── application_exceptions.py
        └── http_error_mapper.py
```

---

### 🧰 `base_exceptions.py`

Define una raíz común para todo el sistema.

```python
# app/interfaces/errors/base_exceptions.py

class GymAppError(Exception):
    """Excepción base de la aplicación. No debe ser lanzada directamente."""

    def __init__(self, message: str, *, code: str = None, context: dict | None = None):
        super().__init__(message)
        self.message = message
        self.code = code or self.__class__.__name__
        self.context = context or {}

    def to_dict(self):
        return {"code": self.code, "message": self.message, "context": self.context}
```

> Esta clase permite **unificar la estructura** de cualquier error, sin importar la capa.

---

## 🧠 3. Excepciones de dominio

Usadas **solo dentro del dominio** (entidades, value objects, reglas de negocio).
Si algo viola una regla de negocio, **se lanza aquí**.

```python
# app/interfaces/errors/domain_exceptions.py

from .base_exceptions import GymAppError

class DomainError(GymAppError):
    """Errores relacionados con las reglas del dominio."""


class InvalidEmailError(DomainError):
    """El formato del correo no cumple las reglas del dominio."""


class DuplicateMemberError(DomainError):
    """El miembro ya existe en el sistema."""
```

### Ejemplo de uso en un Value Object:

```python
# app/domain/members/value_objects/email.py
import re
from app.interfaces.errors.domain_exceptions import InvalidEmailError

class Email:
    def __init__(self, value: str):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise InvalidEmailError(f"Formato de email inválido: {value}")
        self.value = value
```

> 🧩 Las excepciones del dominio no deberían “saber” de HTTP ni de persistencia.
> Solo comunican **violaciones a las reglas del negocio**.

---

## ⚙️ 4. Excepciones de aplicación

Definen errores **operacionales**, como conflictos de estado o flujos inválidos.

```python
# app/interfaces/errors/application_exceptions.py
from .base_exceptions import GymAppError

class ApplicationError(GymAppError):
    """Errores que ocurren en la lógica de aplicación."""


class MemberAlreadyExistsError(ApplicationError):
    """Se intentó registrar un miembro que ya existe."""


class MemberNotFoundError(ApplicationError):
    """No se encontró el miembro solicitado."""
```

> ⚠️ Estos errores **no son bugs**, sino **respuestas esperadas** a situaciones del negocio.

### Ejemplo de uso:

```python
# app/application/use_cases/register_member.py
from app.interfaces.errors.application_exceptions import MemberAlreadyExistsError

class RegisterMemberUseCase:
    def __init__(self, member_repository):
        self.member_repository = member_repository

    def execute(self, data: dict):
        if self.member_repository.get_by_email(data["email"]):
            raise MemberAlreadyExistsError("El miembro ya está registrado.")
        ...
```

---

## 🧩 5. Cuándo lanzar y cuándo retornar `None` o `False`

| Situación                                      | Acción recomendada                           | Capa                     |
| ---------------------------------------------- | -------------------------------------------- | ------------------------ |
| Violación de regla de negocio                  | Lanzar excepción (ej. `InvalidEmailError`)   | Dominio                  |
| Error lógico de flujo de aplicación            | Lanzar excepción (ej. `MemberNotFoundError`) | Application              |
| Falla técnica (DB, red, etc.)                  | Lanzar excepción o loggear y propagar        | Infraestructura          |
| Caso esperado (p. ej. búsqueda sin resultados) | Retornar `None` o lista vacía                | Repositorio o aplicación |
| Validación de input HTTP                       | Devolver respuesta 422 (FastAPI)             | Controlador              |

> 🔹 “Excepciones para errores excepcionales; `None` para resultados esperados”.

---

## 🌐 6. Mapeo de errores a HTTP

Toda excepción debe poder traducirse a un `HTTPException` coherente.
Esto se hace en un **mapper centralizado**.

```python
# app/interfaces/errors/http_error_mapper.py
from fastapi import HTTPException, status
from .application_exceptions import *
from .domain_exceptions import *

def map_error_to_http(error: Exception) -> HTTPException:
    match error:
        case MemberAlreadyExistsError():
            return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))
        case MemberNotFoundError():
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
        case InvalidEmailError():
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
        case _:
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor.")
```

Y se usa así en los controladores:

```python
# app/interfaces/controllers/members_controller.py
from fastapi import APIRouter
from app.interfaces.errors.http_error_mapper import map_error_to_http

router = APIRouter()

@router.post("/members/")
def register_member(data: dict, use_case=Depends(register_member_use_case)):
    try:
        member = use_case.execute(data)
        return {"id": member.id, "name": member.name}
    except Exception as e:
        raise map_error_to_http(e)
```

---

## 🧱 7. Error Object Pattern

Este patrón permite **devolver errores como objetos**, no como excepciones.
Útil cuando quieres componer errores o validar múltiples reglas.

```python
# app/domain/shared/result.py
from typing import Generic, TypeVar, Union

T = TypeVar("T")
E = TypeVar("E")

class Result(Generic[T, E]):
    def __init__(self, value: Union[T, None], error: Union[E, None]):
        self.value = value
        self.error = error

    @property
    def is_ok(self) -> bool:
        return self.error is None

    @classmethod
    def ok(cls, value: T):
        return cls(value, None)

    @classmethod
    def fail(cls, error: E):
        return cls(None, error)
```

### Ejemplo de uso:

```python
result = use_case.execute(data)
if not result.is_ok:
    raise map_error_to_http(result.error)
return result.value
```

> 💡 Muy usado en **DDD funcional** y para **validaciones compuestas**.

---

## 🧭 8. Application Error Codes

Conviene asignar **códigos únicos** a los errores para depuración, soporte o frontend.

```python
# app/interfaces/errors/error_codes.py
class ErrorCodes:
    MEMBER_ALREADY_EXISTS = "E001"
    MEMBER_NOT_FOUND = "E002"
    INVALID_EMAIL = "E003"
```

Y los usamos en las excepciones:

```python
class MemberAlreadyExistsError(ApplicationError):
    def __init__(self, message="El miembro ya está registrado."):
        super().__init__(message, code="E001")
```

Así, las respuestas HTTP quedan así:

```json
{
  "code": "E001",
  "message": "El miembro ya está registrado."
}
```

> 🔍 Esto facilita el **logging estructurado** y la trazabilidad en producción.

---

## 🧩 9. Logging y monitoreo de errores

Cada excepción que llegue al mapper debe registrarse.
FastAPI permite añadir un middleware global para esto.

```python
# app/interfaces/middleware/error_logger.py
import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from app.interfaces.errors.http_error_mapper import map_error_to_http

logger = logging.getLogger(__name__)

async def error_handling_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        http_exc = map_error_to_http(e)
        logger.error(f"{type(e).__name__}: {str(e)}", exc_info=True)
        return JSONResponse(status_code=http_exc.status_code, content={"detail": http_exc.detail})
```

> 🔥 Esto asegura trazabilidad sin saturar los controladores.

---

## ✅ 10. Beneficios de esta convención

1. **Claridad semántica:** cada error dice *por qué* ocurrió.
2. **Mantenibilidad:** el equipo no improvisa con `ValueError`.
3. **Observabilidad:** todos los errores son logeables y trazables.
4. **Escalabilidad:** los mapeos HTTP son uniformes.
5. **Desac acoplamiento:** las capas no dependen de FastAPI ni HTTP.

---

## 🧠 Conclusión

En Clean Architecture, los errores no son un detalle técnico:
son **parte del lenguaje del dominio**.
Tratar las excepciones como parte del modelo hace el sistema **expresivo, resiliente y predecible**.

---

## 🧩 PARTE 8 — Inyección de Dependencias

### 1. Principios Fundamentales

**Objetivo:**
Gestionar las dependencias de forma centralizada y explícita, de modo que:

* Cada clase o servicio declare sus dependencias a través del constructor (inyección explícita).
* No haya acoplamientos ocultos ni imports cruzados.
* Se facilite el *testing unitario*, sustituyendo fácilmente dependencias reales por mocks o fakes.

**Beneficios:**

1. **Desacoplamiento total** entre capas.
2. **Sustitución transparente** de implementaciones (por ejemplo, de `SQLMemberRepository` a `InMemoryMemberRepository`).
3. **Configuración centralizada** (un único contenedor gestiona wiring, base de datos, settings, etc.).
4. **Testabilidad y mantenibilidad mejoradas**.

---

### 2. Estructura General del Contenedor

En un proyecto con Clean Architecture, el contenedor suele vivir en `infrastructure/containers.py`.
Este es el “módulo raíz” donde se definen las dependencias de toda la aplicación.

```
src/
├── gym_app/
│   ├── application/
│   ├── domain/
│   ├── infrastructure/
│   │   ├── repositories/
│   │   ├── database/
│   │   ├── containers.py  👈
│   ├── interfaces/
│   │   ├── api/
│   │   │   ├── members_controller.py
│   │   │   ├── router.py
│   │   │   └── errors.py
│   ├── main.py
```

---

### 3. Configuración del Contenedor con Dependency Injector

#### 3.1 Ejemplo: `containers.py`

```python
# gym_app/infrastructure/containers.py
from dependency_injector import containers, providers
from gym_app.infrastructure.database import Database
from gym_app.infrastructure.repositories.members_repository import SQLMemberRepository
from gym_app.application.use_cases.members import (
    CreateMemberUseCase, GetMemberByIdUseCase
)

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["gym_app.interfaces.api.members_controller"]
    )

    # 1️⃣ Infraestructura base
    config = providers.Configuration()
    db = providers.Singleton(Database, db_url=config.db.url)

    # 2️⃣ Repositorios
    member_repository = providers.Factory(
        SQLMemberRepository,
        session_factory=db.provided.session
    )

    # 3️⃣ Casos de uso (Application Layer)
    create_member_use_case = providers.Factory(
        CreateMemberUseCase,
        repository=member_repository
    )
    get_member_by_id_use_case = providers.Factory(
        GetMemberByIdUseCase,
        repository=member_repository
    )
```

**Notas importantes:**

* `providers.Singleton`: instancia única (ideal para DB, cache, etc.).
* `providers.Factory`: crea una nueva instancia por solicitud (ideal para casos de uso).
* `wiring_config`: indica los módulos donde se realizará la inyección automática.

---

### 4. Wiring en el Controlador FastAPI

#### 4.1 Ejemplo de `members_controller.py`

```python
# gym_app/interfaces/api/members_controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide
from gym_app.infrastructure.containers import Container
from gym_app.application.use_cases.members import (
    CreateMemberUseCase, GetMemberByIdUseCase
)
from gym_app.interfaces.api.schemas import MemberCreateRequest, MemberResponse

router = APIRouter(prefix="/members", tags=["Members"])

@router.post("/", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
@inject
async def create_member(
    request: MemberCreateRequest,
    use_case: CreateMemberUseCase = Depends(Provide[Container.create_member_use_case]),
):
    try:
        member = await use_case.execute(request.name, request.email)
        return MemberResponse.from_domain(member)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{member_id}", response_model=MemberResponse)
@inject
async def get_member(
    member_id: int,
    use_case: GetMemberByIdUseCase = Depends(Provide[Container.get_member_by_id_use_case]),
):
    member = await use_case.execute(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return MemberResponse.from_domain(member)
```

🔹 Aquí los controladores no crean nada manualmente:
`Dependency Injector` se encarga de proporcionar las instancias correctas de los casos de uso con sus dependencias ya inyectadas.

🔹 Este patrón se traduce en:

* Menor acoplamiento.
* Mejor legibilidad del flujo de dependencias.
* Control centralizado de wiring.

---

### 5. Inyección en `main.py`

El punto de entrada de la app registra el contenedor y lo vincula con FastAPI.

```python
# gym_app/main.py
from fastapi import FastAPI
from gym_app.infrastructure.containers import Container
from gym_app.interfaces.api.router import router as api_router

def create_app() -> FastAPI:
    container = Container()
    container.config.db.url.from_env("DATABASE_URL")

    app = FastAPI(title="GymApp Clean Architecture")
    app.container = container  # 🔗 vinculación

    app.include_router(api_router)

    return app

app = create_app()
```

---

### 6. Patrones de Inyección por Contexto

| Contexto                               | Provider recomendado                                | Justificación                        |
| -------------------------------------- | --------------------------------------------------- | ------------------------------------ |
| Base de datos, Redis, Cache            | `Singleton`                                         | Recursos compartidos y costosos.     |
| Casos de uso / Servicios de aplicación | `Factory`                                           | Cada request usa su propio contexto. |
| Repositorios                           | `Factory` o `Singleton` (según si comparten sesión) | Depende de la estrategia de sesión.  |
| Configuración                          | `Configuration`                                     | Centraliza settings globales.        |

---

### 7. Testing con Dependency Injector

Ejemplo de *override* para testear un caso de uso con repositorio fake.

```python
# tests/conftest.py
import pytest
from gym_app.infrastructure.containers import Container
from gym_app.tests.fakes import InMemoryMemberRepository

@pytest.fixture
def container():
    container = Container()
    container.member_repository.override(
        providers.Factory(InMemoryMemberRepository)
    )
    yield container
    container.unwire()
```

De este modo, los tests usan un repositorio en memoria sin tocar la base de datos real.

---

### 8. Mejores Prácticas

1. **Nunca instanciar manualmente dependencias** fuera del contenedor.
2. **No inyectar dentro del dominio.**

   * El dominio debe ser puro.
   * Solo la capa de aplicación o infraestructura usa DI.
3. **Evitar imports cruzados** entre módulos inyectados.
4. **Registrar wiring por módulo, no por función.**
5. **Separar configuraciones de entorno** (por ejemplo, `containers_dev.py`, `containers_test.py`).

---

### 9. Conexión con la Filosofía General

La inyección de dependencias es el **puente invisible** que une todas las capas sin violar el principio de inversión de dependencias (D de SOLID).
Es el equivalente a decir:

> “El dominio no sabe quién lo usa, y la infraestructura no necesita saber qué lógica ejecuta.”

Así, cada capa permanece libre y sustituible, lo que es la esencia de Clean Architecture.

---

Perfecto, Marcos.
Entonces esta **Parte 9: Modelo de Trabajo** cerrará la guía práctica del módulo `members`, integrando todo lo que vimos antes (filosofía, dominio, aplicación, infraestructura, controladores, excepciones y testing).

El propósito de esta parte es **definir cómo se organiza el flujo de trabajo completo en un proyecto basado en Clean Architecture**, tanto desde una perspectiva técnica como operativa (cómo se trabaja día a día, cómo se crean nuevas features, cómo se testean, etc.).

---

## 🧩 PARTE 9 — MODELO DE TRABAJO

*(Basado en el módulo `members` y aplicable al resto de módulos del sistema)*

---

### 1. Filosofía General de Trabajo

Antes de escribir una sola línea de código, el equipo debe **pensar en términos de dominio**:

1. **El negocio primero:**
   Cada nueva funcionalidad comienza con la comprensión del lenguaje del dominio (qué significa un “miembro”, qué acciones realiza, qué reglas debe cumplir).
   → Esto se traduce en entidades, value objects y servicios de dominio.

2. **Arquitectura como contrato, no como burocracia:**
   Cada capa tiene responsabilidades claras. Saltar capas o mezclar responsabilidades es un “code smell”.

3. **Diseño guiado por pruebas (TDD o ATDD):**
   Siempre que sea posible, los casos de uso y reglas de dominio deben desarrollarse partiendo de tests.

4. **Independencia de frameworks:**
   FastAPI, SQLModel, Dependency Injector, etc., son implementaciones intercambiables.
   El código del dominio y la aplicación deben sobrevivir aunque cambie la infraestructura.

---

### 2. Flujo de Desarrollo de una Nueva Feature

Supongamos que agregamos un caso de uso: **“Actualizar el email de un miembro”**.

#### 🧱 Paso 1: Dominio

* Revisar si el agregado `Member` y el value object `Email` ya contemplan las validaciones necesarias.
* Si no, se modifica el `Email` value object y se añaden excepciones semánticas (por ejemplo, `InvalidEmailError`).

#### ⚙️ Paso 2: Caso de Uso (Aplicación)

* Crear un nuevo use case: `update_member_email.py` dentro de `application/use_cases/mutations/`.
* Inyectar el repositorio `IMemberRepository` y llamar a los métodos de dominio que correspondan.
* No lanzar errores HTTP ni retornar JSON aquí —solo objetos de dominio o DTOs.

#### 🏗️ Paso 3: Infraestructura

* Implementar el método `update_email()` en `SQLModelMemberRepository`, dentro de la capa `infrastructure`.
* Manejar posibles excepciones de base de datos (por ejemplo, `IntegrityError` → `DuplicateEmailError`).

#### 🌐 Paso 4: Controlador (FastAPI)

* Crear el endpoint `PUT /members/{id}/email` en `interfaces/api/v1/members_controller.py`.
* Inyectar el caso de uso con `Dependency Injector`.
* Capturar excepciones del dominio y convertirlas a respuestas HTTP:

  ```python
  @router.put("/{member_id}/email", response_model=MemberResponse)
  async def update_member_email(
      member_id: UUID,
      command: UpdateMemberEmailCommand,
      use_case: UpdateMemberEmailUseCase = Depends(Provide[Container.update_member_email_use_case])
  ):
      try:
          return await use_case.execute(member_id, command.email)
      except DuplicateEmailError as e:
          raise HTTPException(status_code=409, detail=str(e))
      except MemberNotFoundError as e:
          raise HTTPException(status_code=404, detail=str(e))
  ```

#### 🧪 Paso 5: Testing

* Crear un `test_update_member_email.py` en `tests/application/use_cases/members/`.
* Testear el caso de uso con un repositorio fake o mock.
* Testear el endpoint completo en `tests/integration/api/test_members_endpoints.py`.

---

### 3. Convenciones de Organización

| Tipo                          | Ubicación                                   | Ejemplo                          | Descripción                              |
| ----------------------------- | ------------------------------------------- | -------------------------------- | ---------------------------------------- |
| **Entidades / VO**            | `domain/models`                             | `member.py`, `email.py`          | Modelos puros, sin dependencias externas |
| **Repositorios (interfaces)** | `domain/repositories`                       | `members_repository.py`          | Contratos abstractos                     |
| **Casos de uso**              | `application/use_cases/{queries,mutations}` | `create_member.py`               | Orquestan lógica del dominio             |
| **Repositorios reales**       | `infrastructure/repositories`               | `sqlmodel_members_repository.py` | Implementaciones concretas               |
| **Controladores**             | `interfaces/api/v1/`                        | `members_controller.py`          | Endpoints FastAPI                        |
| **Schemas (DTOs)**            | `interfaces/api/v1/schemas`                 | `member_response.py`             | Modelos Pydantic para I/O                |
| **Tests**                     | `tests/{unit,integration}`                  | `test_create_member.py`          | Validan comportamiento                   |

---

### 4. Buenas Prácticas Operativas

1. **Cada módulo (`members`, `subscriptions`, `payments`, etc.) es autocontenible.**
   Contiene su dominio, aplicación, infraestructura y controladores.

2. **Usar Dependency Injector como capa de ensamblaje.**
   La composición (wiring) se realiza en `main.py` o `container.py`.
   Ninguna otra capa debe crear dependencias manualmente.

3. **Feature toggles y flags** deben gestionarse a nivel de infraestructura, nunca dentro del dominio.

4. **Logs y métricas** se manejan en `infrastructure/logging` o `infrastructure/monitoring`,
   y se integran en casos de uso solo mediante interfaces.

5. **Testing continuo:**
   Cada nuevo caso de uso debe venir con sus tests unitarios.
   Los tests de integración deben validarse al menos una vez antes de hacer merge.

---

### 5. Flujo de Entrega (CI/CD Simplificado)

1. **Commit & Lint:**
   Ejecutar `black`, `isort`, `ruff`, `pytest --maxfail=1`.

2. **Pipeline CI:**

   * Tests unitarios
   * Tests de integración
   * Verificación de cobertura mínima (≥ 90%)
   * Revisión de convenciones de arquitectura (import paths, dependencias)

3. **Deploy:**

   * Se construye la imagen Docker.
   * El contenedor se inicia con `main.py` y el wiring de dependencias completo.
   * Variables sensibles (`DATABASE_URL`, `SECRET_KEY`, etc.) en `.env`.

---

### 6. Extensibilidad del Modelo de Trabajo

Cuando se agregue un nuevo módulo (por ejemplo, `subscriptions`), basta con:

1. Duplicar la estructura de `members`.
2. Cambiar nombres de dominio y entidades.
3. Crear interfaces y casos de uso específicos.
4. Enlazar en `container.py` (inyección de dependencias).
5. Añadir endpoints en `interfaces/api/v1/subscriptions_controller.py`.

De esta manera, el sistema crece de forma modular, sin romper la arquitectura.
