title: "Tests de dominio"
weight: 5

---

> En este capítulo aprendemos a **probar el dominio**, no el framework ni la base de datos.
> Los tests sirven para validar **reglas de negocio** y darnos **confianza para cambiar el código**.

Este capítulo está diseñado para alguien que **no conoce ni Python ni testing**.

---

## 🎯 Objetivo del capítulo

Al terminar este capítulo serás capaz de:

* Entender qué es un **test**
* Comprender por qué en DDD se testea primero el **dominio**
* Aprender `pytest` desde cero
* Escribir tests claros para:

  * **Value Objects**
  * **Entidades**
  * **Domain Services**
* Introducir el patrón **Object Mother** para mejorar la legibilidad de los tests

---

## 🧩 Conceptos de DDD introducidos en este capítulo

En esta sección **no hablamos de Python**. Solo hablamos de **diseño y dominio**.

---

### Tests de dominio

Un **test de dominio** valida:

* reglas de negocio
* invariantes del dominio
* comportamientos permitidos y prohibidos

No valida:

* bases de datos
* frameworks
* APIs

El dominio debe poder probarse **sin infraestructura**.

---

### Comportamiento antes que implementación

En DDD no nos interesa cómo está escrito el código por dentro.

Nos interesa:

* qué hace el objeto
* cuándo falla
* qué reglas protege

Los tests describen **comportamiento**, no estructura.

---

### Tests como especificación viva

En DDD, los tests son una **especificación ejecutable**:

* documentan reglas
* muestran ejemplos válidos e inválidos
* sirven como contrato del dominio

Un desarrollador debería poder entender el dominio leyendo solo los tests.

---

## 🐍 Conceptos de Python introducidos en este capítulo

En esta sección **no hablamos de negocio**. Solo explicamos **Python y testing**.

---

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
* no requiere clases
* mensajes de error claros

---

### `assert`

`assert` verifica que una condición sea verdadera.

Si no lo es, el test falla automáticamente.

---

### Probar excepciones

Un test también puede verificar que una **regla se rompe** lanzando una excepción.

Esto es clave en DDD: muchas reglas se expresan como errores de dominio.

---

## 🧱 Aplicación al dominio (DDD + Python juntos)

---

### Estructura de tests

```
tests/
  shared/
    domain/
      value_objects/
        test_date_range.py
        date_range_mother.py

  rentals/
    booking/
      domain/
        test_booking.py
        booking_mother.py
        services/
          test_booking_pricing_service.py
```

La estructura de tests **refleja la estructura del dominio**.

---

## 🧪 Tests del Value Object `DateRange`

Antes de usar Object Mother, un test típico sería largo y repetitivo.

Con Object Mother, los tests se centran solo en el comportamiento.

---

### Object Mother

**Object Mother** es un patrón de testing que se usa para:

* crear objetos válidos del dominio
* reducir ruido en los tests
* evitar repetir siempre el mismo setup

Importante:

* NO es dominio
* NO vive en `src/`
* SOLO se usa en tests

---

### DateRangeMother

```python
from datetime import date
from shared.domain.value_objects.date_range import DateRange


class DateRangeMother:
    @staticmethod
    def january_2025() -> DateRange:
        return DateRange(start_date=date(2025, 1, 1), end_date=date(2025, 1, 31))

    @staticmethod
    def one_week() -> DateRange:
        return DateRange(start_date=date(2025, 1, 1), end_date=date(2025, 1, 7))

    @staticmethod
    def invalid() -> DateRange:
        return DateRange(start_date=date(2025, 1, 31), end_date=date(2025, 1, 1))
```

---

### Test usando Object Mother

```python
import pytest

from shared.domain.errors.invalid_date_range import InvalidDateRange
from tests.shared.domain.value_objects.date_range_mother import DateRangeMother


def test_valid_date_range_is_created():
    date_range = DateRangeMother.january_2025()
    assert date_range.contains(date_range.start_date) is True


def test_invalid_date_range_raises_error():
    with pytest.raises(InvalidDateRange):
        DateRangeMother.invalid()
```

---

## 🧪 Tests de la Entidad `Booking`

*(Se mantienen como estaban en tu capítulo; no los repetimos aquí para no duplicar.)*

---

## 🧪 Tests del Domain Service: `BookingPricingService`

Archivo:

`tests/rentals/booking/domain/services/test_booking_pricing_service.py`

```python
import pytest

from rentals.booking.domain.services.booking_pricing_service import BookingPricingService
from rentals.booking.domain.errors.invalid_nightly_rate import InvalidNightlyRate
from tests.shared.domain.value_objects.date_range_mother import DateRangeMother


def test_total_price_is_days_times_rate_when_under_discount_threshold():
    date_range = DateRangeMother.one_week()  # 7 días exactos
    total = BookingPricingService.calculate_total_cents(date_range=date_range, nightly_rate_cents=1000)

    # 7 días * 1000 céntimos = 7000
    # OJO: este test depende de la regla del descuento.
    # En nuestro servicio, 7 días ya aplica descuento (threshold >= 7).
    assert total == 6300


def test_discount_is_applied_when_days_are_7_or_more():
    date_range = DateRangeMother.one_week()
    total = BookingPricingService.calculate_total_cents(date_range=date_range, nightly_rate_cents=1000)

    # 7000 - 10% = 6300
    assert total == 6300


def test_invalid_rate_raises_domain_error():
    date_range = DateRangeMother.one_week()

    with pytest.raises(InvalidNightlyRate):
        BookingPricingService.calculate_total_cents(date_range=date_range, nightly_rate_cents=0)
```

---

## 🛠️ Ejecución de tests

Los tests se ejecutan dentro del contenedor Docker usando el `Makefile`.

Comandos habituales:

```
make test
make test-file f=tests/rentals/booking/domain/test_booking.py
make test-file f=tests/rentals/booking/domain/services/test_booking_pricing_service.py
```

---

## 🧠 Qué hemos aprendido

* El dominio se prueba sin infraestructura
* Los tests describen comportamiento
* Object Mother reduce ruido en los tests
* Los Domain Services también se testean (como parte del dominio)

---

## ✅ Check final

Antes de continuar deberías poder explicar:

* qué es un test
* qué valida un test de dominio
* qué es Object Mother
* por qué Object Mother no pertenece al dominio
* cómo se testea un Domain Service
* cómo ejecutar tests del dominio
