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
* Entender cuando usar DTO y cuando no
* Saber por qué el Application Layer existe
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

El Application Layer:

* coordina el dominio
* ejecuta casos de uso
* gestiona transacciones

Pero:

* no contiene reglas de negocio
* no conoce detalles técnicos

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

### Métodos públicos

El método público del caso de uso:

* recibe datos de entrada encapsulados en un DTO
* ejecuta la intención
* devuelve un resultado simple (si aplica)

---

## 🧱 Aplicación al proyecto (DDD + Python juntos)

---

### Estructura del Application Layer

```
src/
  rentals/
    booking/
      application/
        /request
          create_booking_request.py
        create_booking.py
```

Cada fichero representa **un caso de uso**.

Como parámetro de entrada, vamos a tener un **DTO** que encapsula los parámetros necesarios

Como parametros de salida, la regla es:

- Si cruzas un boundary (API ↔ Application) y devuelves más de un valor o quieres un contrato estable
  - ✅ Output DTO
- Si el caso de uso devuelve un único valor simple (p. ej. UUID) y te vale como contrato
  - ✅ puedes devolver el valor directamente sin DTO.
  
---
### Cómo queda la comunicación “correcta”
✅ **API → Application**
    - API recibe CreateBookingRequest (DTO)
    - Lo convierte a tipos del dominio o a un input del caso de uso

✅ **Application → API**
    - Application devuelve CreateBookingResult (DTO de salida) o algo simple (booking_id)
    - API decide cómo responder (201 + Location + body)


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

### Implementación del DTO (Request)
```
from datetime import date


class CreateBookingRequest:
    def __init__(self, start_date: date, end_date: date):
        self.start_date = start_date
        self.end_date = end_date
```
### Implementación del caso de uso

```
from datetime import date
from uuid import UUID

from rentals.booking.domain.booking import Booking
from shared.domain.value_objects.date_range import DateRange
from rentals.booking.application.request.create_booking_request import CreateBookingRequest


class CreateBooking:
    def execute(self, request: CreateBookingRequest) -> UUID:
        date_range = DateRange(request.start_date, request.end_date)
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
* El dominio no depende de la aplicación
* Los casos de uso no son controladores

---

## ✅ Check final

Antes de continuar deberías poder explicar:

* qué es un caso de uso
* qué problema resuelve el Application Layer
* por qué el dominio no depende de la aplicación
* por qué el caso de uso devuelve solo un ID

---

En el siguiente capítulo veremos cómo **persistir** lo que hemos creado:

➡️ **3.3 — Tests de Application Layer**
