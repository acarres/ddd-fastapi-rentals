---

title: "Casos de uso"
weight: 6
---------

> En este capítulo damos el paso clave entre **el dominio** y **la aplicación real**.
> Aprendemos a expresar **qué quiere hacer el sistema**, sin mezclar negocio, framework ni persistencia.

Este capítulo está diseñado para alguien que **no conoce ni DDD ni Python**, pero ya entiende:

* qué es una Entidad
* qué es un Value Object
* qué es un test de dominio

---

## 🎯 Objetivo del capítulo

Al terminar este capítulo serás capaz de:

* Entender qué es un **caso de uso**
* Entender **cuándo usar DTO y cuándo no**
* Saber por qué el **Application Layer** existe
* Diferenciar **intención** de **ejecución**
* Implementar un primer caso de uso en Python
* Ver cómo el dominio se usa sin ser modificado

---

## 🧩 Conceptos de DDD introducidos en este capítulo

En esta sección **no hablamos de Python**.
Solo hablamos de **arquitectura y responsabilidades**.

---

### Qué es un caso de uso

Un **caso de uso** representa una **intención del usuario o del sistema**.

Ejemplos:

* crear una reserva
* cancelar una reserva
* finalizar una reserva

Un caso de uso:

* describe **qué se quiere hacer**
* orquesta objetos del dominio
* no contiene reglas de negocio complejas

---

### Qué NO es un caso de uso

Un caso de uso NO es:

* un controlador HTTP
* un endpoint
* una clase de dominio
* una consulta a base de datos

El caso de uso **no sabe**:

* cómo llega la petición
* cómo se guarda en la base de datos
* cómo se devuelve la respuesta

---

### Application Layer como orquestador

El **Application Layer**:

* coordina el dominio
* ejecuta casos de uso
* define fronteras claras

Pero:

* no contiene reglas de negocio
* no conoce detalles técnicos

---

### DTO como frontera de entrada

Un **DTO (Data Transfer Object)** representa los **datos de entrada o salida** de un caso de uso.

En este curso:

* el DTO **no es dominio**
* no protege invariantes
* no contiene lógica
* solo expresa la **intención del cliente**

> El dominio **no conoce** los DTOs.

---

### DTO de entrada vs DTO de salida

La regla que seguiremos es:

* Si cruzas un boundary (API ↔ Application) y devuelves **más de un valor** o quieres un contrato estable

  * ✅ usa un **DTO de salida**
* Si el caso de uso devuelve un único valor simple (por ejemplo un `UUID`)

  * ✅ puedes devolver ese valor directamente

---

## 🐍 Conceptos de Python introducidos en este capítulo

En esta sección **no hablamos de negocio**.
Solo explicamos **el lenguaje Python**.

---

### Clases de servicio simples

En Python, un caso de uso suele representarse como una **clase con un método público**.

No es un "service" genérico.
Es una clase que representa **una acción concreta**.

---

### `@dataclass`

`@dataclass` permite definir clases simples sin escribir código repetitivo.

En este capítulo lo usamos para:

* definir DTOs
* dejar claro que son solo datos

---

### `frozen=True`

Hace que el objeto sea **inmutable**.

Esto es importante porque:

* un DTO no debería cambiar una vez creado
* evita efectos secundarios

---

## 🧱 Aplicación al proyecto (DDD + Python juntos)

---

### Estructura del Application Layer

```
src/
  rentals/
    booking/
      application/
        create_booking.py
        create_booking_request.py
```

Cada fichero representa **una responsabilidad clara**.

---

## 🧭 Caso de uso: Crear una reserva

### Intención

> "Quiero crear una reserva con un rango de fechas"

No decimos:

* cómo llega la petición
* cómo se guarda
* cómo se devuelve

Solo expresamos la intención.

---

### Implementación del DTO de entrada

```python
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class CreateBookingRequest:
    start_date: date
    end_date: date
```

Este DTO:

* vive en Application Layer
* no contiene lógica
* no valida reglas de negocio

---

### Implementación del caso de uso

```python
from uuid import UUID

from rentals.booking.domain.booking import Booking
from shared.domain.value_objects.date_range import DateRange
from rentals.booking.application.create_booking_request import CreateBookingRequest


class CreateBooking:
    def execute(self, request: CreateBookingRequest) -> UUID:
        date_range = DateRange(
            request.start_date,
            request.end_date,
        )

        # Nota: por ahora el ID se genera dentro del dominio.
        # Más adelante veremos otras estrategias (client-generated IDs, CQRS).
        booking = Booking.create(date_range)

        return booking.id
```

Este caso de uso:

* crea los objetos necesarios
* usa el dominio
* no persiste nada todavía
* devuelve solo el identificador

---

## 🧠 Decisiones importantes (explicadas)

### Por qué el caso de uso devuelve solo el ID

El caso de uso **no devuelve el aggregate completo**.

Devuelve:

* el identificador de la entidad creada

Esto es importante porque:

* evita acoplar escritura y lectura
* prepara el camino para CQRS
* permite APIs limpias

Este tema se desarrollará en profundidad en capítulos posteriores.

---

## 🧭 Qué NO estamos haciendo todavía

En este capítulo **intencionadamente NO introducimos**:

* repositorios
* unit of work
* transacciones
* CQRS

Primero necesitamos entender **la intención**.

---

## 🧠 Qué hemos aprendido

* Un caso de uso representa una intención
* El Application Layer orquesta el dominio
* Los DTOs definen fronteras claras
* El dominio no depende de la aplicación

---

## ✅ Check final

Antes de continuar deberías poder explicar:

* qué es un caso de uso
* cuándo usar un DTO
* por qué un DTO no es dominio
* por qué el caso de uso devuelve solo un ID
