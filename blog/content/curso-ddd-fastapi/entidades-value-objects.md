---

title: "Entidades y Value Objects"
weight: 3
---------

> En este capítulo empezamos a escribir **código**, pero manteniendo una separación estricta entre:
>
> * **qué es negocio (DDD)**
> * **qué es lenguaje (Python)**

Este capítulo está diseñado para alguien que **no conoce ni DDD ni Python**.

---

## 🎯 Objetivo del capítulo

* Entender qué son **Entidades** y **Value Objects** en DDD
* Entender qué problemas resuelven
* Aprender cómo se representan en **Python desde cero**
* Construir el primer modelo de dominio **correcto y protegido**

---

## 🧩 Conceptos de DDD introducidos en este capítulo

En esta sección **no hablamos de Python**.
Solo hablamos de **modelado del dominio**.

---

### Entidad

Una **Entidad** es un concepto del dominio que:

* tiene identidad propia
* sigue siendo el mismo aunque cambien sus datos
* puede cambiar con el tiempo

Ejemplos en el mundo real:

* un contrato
* una reserva
* una persona

En nuestro dominio, `Booking` es una **Entidad**.

---

### Value Object

Un **Value Object** es un concepto del dominio que:

* no tiene identidad
* se define solo por sus valores
* es **inmutable**
* protege reglas del negocio

Ejemplos:

* un rango de fechas
* un precio
* una dirección

En nuestro dominio, `DateRange` es un **Value Object**.

---

### Invariantes

Una **invariante** es una regla del dominio que **nunca puede romperse**.

Ejemplo:

* la fecha de inicio debe ser anterior a la fecha de fin

Si una invariante se rompe, el objeto **no debe existir**.

---

### Estados del dominio

Algunos conceptos del dominio tienen **estados finitos**.

Ejemplo:

* una reserva puede estar `ACTIVE`, `CANCELLED` o `FINISHED`

Un estado:

* no es texto libre
* define qué operaciones están permitidas

---

### Errores de dominio

Un **error de dominio** representa una regla del negocio que se ha violado.

* no es un error técnico
* es una decisión del negocio
* forma parte del modelo del dominio

---

### Shared (Shared Kernel)

`shared` contiene conceptos:

* genéricos
* reutilizables
* independientes de un dominio concreto

Ejemplos:

* `DateRange`
* `DomainError`

---

## 🧠 Patrones de DDD que ya estás usando (sin formalizar aún)

En este capítulo **ya aparecen patrones clásicos de DDD**, aunque todavía no los hemos presentado como tales.

No los desarrollamos aquí a propósito: primero necesitamos un modelo **simple, correcto y comprensible**.

Esta sección sirve solo para **poner nombre a decisiones que ya hemos tomado**.

---

### Factory (creación controlada de entidades)

El método:

```
Booking.create(date_range)
```

es un ejemplo simple del patrón **Factory**.

En lugar de permitir crear la entidad directamente con cualquier estado inicial, usamos un método que:

* controla cómo nace la entidad
* garantiza un estado inicial válido
* centraliza reglas de creación

Más adelante veremos **Factories dedicadas** cuando la creación sea más compleja.

---

### Estados modelados explícitamente

`BookingStatus` no es un `str`.

Representa un **conjunto cerrado de estados válidos**, lo que evita:

* valores inválidos
* comparaciones frágiles
* estados inconsistentes

Este enfoque prepara el terreno para patrones como **Policy / Strategy**, que veremos más adelante.

---

### Errores de dominio como parte del modelo

Errores como:

* `InvalidDateRange`
* `BookingNotActive`

no son excepciones técnicas.

Son **reglas de negocio expresadas como código**.

Este enfoque:

* hace el dominio más explícito
* obliga a respetar las reglas
* prepara el terreno para **Domain Events** en capítulos posteriores

---

### Por qué las entidades no exponen setters

En DDD, una entidad **no es una estructura de datos**.

Es un objeto que **protege reglas de negocio**.

Por eso:

* el estado no se modifica libremente
* no existen setters genéricos
* los cambios se hacen mediante métodos con significado de negocio

Ejemplo:

❌ Incorrecto:

```
booking.set_status("cancelled")
```

✅ Correcto:

```
booking.cancel()
```

Esto garantiza que:

* las invariantes se respetan
* los estados inválidos no existen
* el dominio se mantiene consistente

---

## 🧱 Aplicación al dominio (DDD + Python juntos)

### Estructura del proyecto

```
src/
  shared/
    domain/
      errors/
        domain_error.py
        invalid_date_range.py
      value_objects/
        date_range.py

  rentals/
    booking/
      domain/
        booking.py
        booking_status.py
        errors/
          booking_not_active.py
```

---

### Error base del dominio

```
from abc import ABC

class DomainError(Exception, ABC):
    """Base class for domain errors."""
    pass
```

---

### Error concreto del dominio

```
from shared.domain.errors.domain_error import DomainError

class InvalidDateRange(DomainError):
    pass
```

---

### Value Object: DateRange

```
from dataclasses import dataclass
from datetime import date

from shared.domain.errors.invalid_date_range import InvalidDateRange

@dataclass(frozen=True)
class DateRange:
    start_date: date
    end_date: date

    def __post_init__(self) -> None:
        if self.start_date > self.end_date:
            raise InvalidDateRange()

    def contains(self, value: date) -> bool:
        return self.start_date <= value <= self.end_date
```

---

### Estado del dominio con Enum

```
from enum import Enum

class BookingStatus(Enum):
    ACTIVE = "ACTIVE"
    CANCELLED = "CANCELLED"
    FINISHED = "FINISHED"
```

---

### Entidad: Booking

```
from dataclasses import dataclass
from uuid import UUID, uuid4

from shared.domain.value_objects.date_range import DateRange
from .booking_status import BookingStatus
from .errors.booking_not_active import BookingNotActive

@dataclass
class Booking:
    id: UUID
    date_range: DateRange
    status: BookingStatus

    @staticmethod
    def create(date_range: DateRange) -> "Booking":
        return Booking(
            id=uuid4(),
            date_range=date_range,
            status=BookingStatus.ACTIVE,
        )

    def cancel(self) -> None:
        if self.status is not BookingStatus.ACTIVE:
            raise BookingNotActive()
        self.status = BookingStatus.CANCELLED
```

---

## 🐍 Conceptos de Python introducidos en este capítulo

En esta sección **no hablamos de negocio**.
Solo explicamos **el lenguaje Python**.

---

### `class`

Permite definir una nueva clase.

---

### `@dataclass`

Genera automáticamente el código necesario para crear, inicializar y comparar objetos que solo contienen datos, evitando escribir siempre lo mismo a mano.

---

### `frozen=True`

Hace que un objeto sea inmutable.

---

### `Enum`

Representa un conjunto cerrado de valores posibles.

---

### `Exception` y `raise`

Permiten lanzar y capturar errores.

---

### Clases abstractas (`ABC`)

Permiten definir clases que **no se pueden instanciar**.

---

### `pass`

Indica un bloque vacío intencional.

---

### `-> "Type"` (type hints)

Indica el tipo de valor que devuelve una función.

---

### `__post_init__`

Método especial de `dataclass` que se ejecuta tras crear el objeto.

---

## ✅ Check final

Antes de continuar deberías poder explicar:

* qué es una Entidad
* qué es un Value Object
* qué es una invariante
* por qué `status` no es un `str`
* qué es `Enum`
* qué es una excepción de dominio
* por qué `DomainError` es abstracta
