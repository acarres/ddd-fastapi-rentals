---
title: "Tests de dominio"
weight: 4
---

> En este capítulo aprendemos a **probar el dominio**, no el framework ni la base de datos.
> Los tests sirven para validar **reglas de negocio** y darnos **confianza para cambiar el código**.

Este capítulo está pensado para alguien que **no conoce ni Python ni testing**.

---

## 🎯 Objetivo del capítulo

* Entender qué es un **test**
* Entender por qué en DDD se testea primero el dominio
* Aprender `pytest` desde cero
* Escribir tests para **Value Objects** y **Entidades**
* Aprender a ejecutar tests de forma cómoda con **Makefile**

---

## 🧩 Conceptos de DDD introducidos en este capítulo

En esta sección **no hablamos de Python**.

### Tests de dominio

Un **test de dominio** verifica:

* reglas de negocio
* invariantes
* comportamientos permitidos y no permitidos

No prueba:

* bases de datos
* APIs
* frameworks

---

### Confianza en el modelo

Un dominio bien testeado permite:

* cambiar código sin miedo
* detectar errores rápidamente
* evolucionar el sistema con seguridad

En DDD, **los tests forman parte del diseño**.

---

### Comportamiento, no implementación

En DDD no nos interesa *cómo* está hecho algo internamente.

Nos interesa:

* qué hace
* cuándo falla
* qué reglas protege

Por eso los tests hablan en **lenguaje del dominio**.

---

## 🐍 Conceptos de Python introducidos en este capítulo

En esta sección **no hablamos de negocio**.

### Qué es un test

Un test es una función que:

* ejecuta código
* comprueba un resultado
* falla si el resultado no es el esperado

---

### `pytest`

`pytest` es una librería de Python para escribir tests.

Ventajas:

* sintaxis simple
* no necesita clases
* mensajes de error claros

---

### `assert`

`assert` comprueba que una condición sea verdadera.

Si no lo es, el test falla.

---

### Excepciones en tests

Un test también puede comprobar que **se lanza un error** cuando una regla se rompe.

Esto es clave para validar reglas de negocio.

---

### Convención de nombres

`pytest` detecta automáticamente:

* archivos que empiezan por `test_`
* funciones que empiezan por `test_`

---

## 🧱 Aplicación al dominio (DDD + Python juntos)

### Estructura de tests

```
tests/
  shared/
    domain/
      value_objects/
        test_date_range.py

  rentals/
    booking/
      domain/
        test_booking.py
```

La estructura de tests **refleja la estructura del dominio**.

---

## 🧪 Tests del Value Object `DateRange`

Archivo:

```
tests/shared/domain/value_objects/test_date_range.py
```

```python
from datetime import date

from shared.domain.value_objects.date_range import DateRange
from shared.domain.errors.invalid_date_range import InvalidDateRange


def test_date_range_is_created_when_dates_are_valid():
    date_range = DateRange(
        start_date=date(2025, 1, 1),
        end_date=date(2025, 1, 31),
    )

    assert date_range.start_date == date(2025, 1, 1)
    assert date_range.end_date == date(2025, 1, 31)


def test_date_range_raises_error_when_end_is_before_start():
    from pytest import raises

    with raises(InvalidDateRange):
        DateRange(
            start_date=date(2025, 1, 31),
            end_date=date(2025, 1, 1),
        )


def test_date_range_contains_date_inside_range():
    date_range = DateRange(
        start_date=date(2025, 1, 1),
        end_date=date(2025, 1, 31),
    )

    assert date_range.contains(date(2025, 1, 15)) is True
    assert date_range.contains(date(2025, 2, 1)) is False
```

---

## 🧪 Tests de la Entidad `Booking`

Archivo:

```
tests/rentals/booking/domain/test_booking.py
```

```python
import pytest
from datetime import date

from rentals.booking.domain.booking import Booking
from rentals.booking.domain.booking_status import BookingStatus
from rentals.booking.domain.errors.booking_not_active import BookingNotActive
from shared.domain.value_objects.date_range import DateRange


def test_booking_is_created_as_active():
    date_range = DateRange(
        start_date=date(2025, 1, 1),
        end_date=date(2025, 1, 31),
    )

    booking = Booking.create(date_range)

    assert booking.status is BookingStatus.ACTIVE


def test_booking_status_is_not_a_free_string():
    date_range = DateRange(
        start_date=date(2025, 1, 1),
        end_date=date(2025, 1, 31),
    )

    booking = Booking.create(date_range)

    assert isinstance(booking.status, BookingStatus)


def test_booking_can_be_cancelled_when_active():
    date_range = DateRange(
        start_date=date(2025, 1, 1),
        end_date=date(2025, 1, 31),
    )

    booking = Booking.create(date_range)
    booking.cancel()

    assert booking.status is BookingStatus.CANCELLED


def test_booking_cannot_be_cancelled_when_not_active():
    date_range = DateRange(
        start_date=date(2025, 1, 1),
        end_date=date(2025, 1, 31),
    )

    booking = Booking.create(date_range)
    booking.cancel()

    with pytest.raises(BookingNotActive):
        booking.cancel()
```

---

## 🛠️ Automatización con Makefile

Los tests se ejecutan **dentro del contenedor Docker**.
Para no tener que recordar comandos largos, usamos un **Makefile**.

Un Makefile define **atajos** para ejecutar tareas repetitivas.

### Variables usadas

* `COMPOSE_FILE` → ruta al archivo `docker-compose.yml`
* `SERVICE` → nombre del servicio Docker donde corre Python (`api`)

---

### Ejecutar todos los tests

```bash
make test
```

Ejecuta todos los tests del proyecto.

---

### Ejecutar un solo fichero

```bash
make test-file f=tests/shared/domain/value_objects/test_date_range.py
```

Ejecuta únicamente ese archivo de tests.

---

### Ejecutar tests por nombre

```bash
make test-k k=date_range
```

Ejecuta solo los tests cuyo nombre contiene ese texto.

---

### Ejecutar un test concreto

```bash
make test-node n=tests/shared/domain/value_objects/test_date_range.py::test_date_range_is_created_when_dates_are_valid
```

Ejecuta un único test exacto.

---

## 🧠 Qué hemos aprendido

* Los tests protegen reglas de negocio
* Los tests describen comportamiento
* El dominio se puede testear sin infraestructura
* Un Makefile simplifica el trabajo diario

---

## ✅ Check final

Antes de continuar deberías poder explicar:

* qué es un test
* qué es `pytest`
* qué hace `assert`
* cómo se prueba una excepción
* cómo ejecutar tests con Makefile

---

## 🔜 Próximo capítulo

En el **Capítulo 05 — Application Layer (Casos de uso)** aprenderemos a:

> orquestar el dominio sin romperlo.

Continuamos 🚀
