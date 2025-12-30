---

title: "Tests de Application Layer"
weight: 7
---------

> En este capítulo aprendemos a **testear casos de uso**.
> No testeamos el dominio ni la infraestructura: testeamos la **orquestación**.

Este capítulo está diseñado para alguien que:

* no conoce Python
* no conoce testing
* pero ya entiende qué es un caso de uso, una Entidad y un Value Object

---

## 🎯 Objetivo del capítulo

Al terminar este capítulo serás capaz de:

* Saber **qué tipo de test** estás escribiendo
* Entender **qué se testea** y **qué no** en Application Layer
* Escribir tests sencillos para casos de uso
* Ver cómo el Application Layer usa el dominio sin duplicar lógica
* Preparar el terreno para introducir doubles en el siguiente bloque

---

## 🧩 Conceptos de DDD introducidos en este capítulo

En esta sección **no hablamos de Python**.
Hablamos de **arquitectura y responsabilidades**.

---

### Qué tipo de test es este

Los tests de este capítulo son:

✅ **Tests de Application Layer**

No son:

❌ tests de dominio (eso ya lo hicimos)
❌ tests de integración
❌ tests de API

---

### Qué prueba un test de Application Layer

Un test de Application Layer verifica que:

* un **caso de uso** se ejecuta correctamente
* el **contrato de entrada** es respetado
* el dominio es **orquestado**, no reimplementado

No verifica:

* reglas internas del dominio
* persistencia
* transporte (HTTP, JSON, etc.)

---

### Qué NO se testea aquí

En estos tests **no probamos**:

* invariantes del dominio
* base de datos real
* framework web

Cada una de esas cosas se testea en su capa correspondiente.

---

## 🐍 Conceptos de Python introducidos en este capítulo

En esta sección **no hablamos de negocio**.
Solo explicamos **testing en Python**.

---

### Qué es `pytest`

`pytest` es una librería de Python para escribir tests.

Características principales:

* los tests son funciones simples
* no hace falta usar clases
* los mensajes de error son claros

---

### `assert`

`assert` comprueba que una condición sea verdadera.

Si no lo es, el test falla.

---

### Excepciones en tests

Un test también puede comprobar que **se lanza una excepción**.

Esto es fundamental para validar flujos erróneos.

---

## 🧱 Aplicación al proyecto (DDD + Python juntos)

---

### Caso de uso a testear

En el capítulo anterior definimos este caso de uso:

```python
class CreateBooking:
    def execute(self, request: CreateBookingRequest) -> UUID:
        ...
```

Este es el objeto que vamos a testear.

---

### DTO de entrada (recordatorio)

El caso de uso recibe un **DTO de entrada** que define su contrato:

```python
from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class CreateBookingRequest:
    start_date: date
    end_date: date
```

---

## 🧪 Test del caso de uso: CreateBooking

Archivo:

```
tests/rentals/booking/application/test_create_booking.py
```

```python
from datetime import date
from uuid import UUID

from rentals.booking.application.create_booking import CreateBooking
from rentals.booking.application.create_booking_request import CreateBookingRequest


def test_create_booking_returns_an_id():
    use_case = CreateBooking()

    booking_id = use_case.execute(
        CreateBookingRequest(
            start_date=date(2025, 1, 1),
            end_date=date(2025, 1, 31),
        )
    )

    assert isinstance(booking_id, UUID)
```

---

### Qué está comprobando este test

Este test verifica que:

* el caso de uso acepta un DTO como entrada
* el dominio se ejecuta correctamente
* el resultado cumple el contrato (un identificador)

No verifica:

* cómo se crea internamente la entidad
* cómo se validan las reglas de negocio

Eso ya está cubierto por los tests de dominio.

---

## 🧪 Test de propagación de error de dominio

Este test comprueba que el Application Layer **no captura ni altera** errores del dominio.

```python
import pytest
from datetime import date
from uuid import UUID

from rentals.booking.application.create_booking import CreateBooking
from rentals.booking.application.create_booking_request import CreateBookingRequest


def test_create_booking_returns_an_id():
    use_case = CreateBooking()
    booking_id = use_case.execute(CreateBookingRequest(start_date=date(2025, 1, 1), end_date=date(2025, 1, 31)))
    assert isinstance(booking_id, UUID)
```

> “No testeamos aquí los errores de dominio porque ya están cubiertos en tests de dominio.
> Volveremos a tests de error cuando el caso de uso tenga lógica propia (repositorio/UoW/mapping).”
---

## 🧠 Nota importante sobre test doubles

En este capítulo **NO usamos todavía**:

* stubs
* fakes
* mocks

¿Por qué?

Porque el caso de uso **todavía no tiene dependencias externas**.

Los doubles aparecerán en el **Bloque 4**, cuando introduzcamos:

* repositorios
* persistencia
* transacciones

---

## 🧠 Qué hemos aprendido

* Los tests de Application Layer prueban **casos de uso**, no reglas
* El DTO define el contrato de entrada
* El Application Layer no duplica lógica del dominio
* No siempre hacen falta doubles

---

## ✅ Check final

Antes de continuar deberías poder explicar:

* qué es un test de Application Layer
* qué se está probando en estos tests
* por qué no se usan mocks todavía
* cómo se testea la propagación de errores
