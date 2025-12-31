---

title: "Servicios de dominio"
weight: 4

---

> En este capítulo introducimos los **Domain Services**: lógica de negocio que **no encaja bien** dentro de una Entidad o un Value Object, pero **sí pertenece al dominio**.

Este capítulo está diseñado para alguien que **no conoce DDD ni Python**, pero ya entiende:

* qué es una Entidad
* qué es un Value Object
* qué es una invariante

---

## 🎯 Objetivo del capítulo

Al terminar este capítulo serás capaz de:

* Entender **qué es un Domain Service**
* Saber **cuándo aparece y cuándo NO usarlo**
* Modelar una regla de negocio “transversal” (que no tiene dueño natural)
* Implementar un Domain Service en Python
* Preparar el terreno para testearlo en el siguiente capítulo

---

## 🧩 Conceptos de DDD introducidos en este capítulo

En esta sección **no hablamos de Python**. Solo hablamos de **diseño del dominio**.

---

### Qué es un Domain Service

Un **Domain Service** es una pieza de dominio que:

* contiene **lógica de negocio**
* no pertenece naturalmente a una Entidad
* no pertenece a un Value Object
* no depende de infraestructura (DB, HTTP, frameworks)

Un Domain Service **no es técnico**. Es **dominio puro**.

---

### Cuándo aparece

Un Domain Service aparece cuando la regla:

* involucra varios conceptos
* o es una operación del negocio que no “vive” bien en un único objeto

Ejemplos típicos:

* cálculo de precios
* políticas de cancelación
* reglas de disponibilidad que dependen de múltiples factores
* validaciones que combinan varios objetos

---

### Qué NO es

Un Domain Service NO es:

* un caso de uso (Application Layer)
* un repositorio (persistencia)
* un servicio técnico
* un “helper” genérico

---

## 🧠 Ejemplo claro: cálculo de precio

Regla de negocio (simplificada para el curso):

1. El precio base es: `días * precio_por_día`
2. Si la estancia dura **7 días o más**, aplicamos **10% de descuento**
3. El precio por día debe ser **positivo**

¿Por qué esto es buen ejemplo de Domain Service?

* No es responsabilidad natural de `DateRange` (ese VO solo protege fechas)
* Tampoco queremos meterlo en `Booking` porque el cálculo puede evolucionar con tarifas, promociones, temporadas…
* Es una regla del negocio, pero “transversal”

👉 Perfecto candidato a **Domain Service**.

---

## 🧱 Aplicación al dominio (DDD + Python juntos)

### Ubicación del Domain Service

```
src/
  rentals/
    booking/
      domain/
        services/
          booking_price_calculator.py
        errors/
          invalid_nightly_rate.py
```

---

### Error de dominio específico

Archivo:

`src/rentals/booking/domain/errors/invalid_nightly_rate.py`

```python
from shared.domain.errors.domain_error import DomainError


class InvalidNightlyRate(DomainError):
    """Se lanza cuando el precio por día no es válido."""
    pass
```

---

### Preparación mínima: un método útil en DateRange

Para poder calcular un precio necesitamos saber “cuántos días dura” un rango.

> Nota de modelado: en este curso, para simplificar, consideramos que el rango es **inclusivo**.
> Por eso sumamos 1 día.

Añade este método en `DateRange`:

```python
from datetime import date


def days(self) -> int:
    return (self.end_date - self.start_date).days + 1
```

---

### Implementación del Domain Service

Archivo:

`src/rentals/booking/domain/services/booking_price_calculator.py`

```python
from shared.domain.value_objects.date_range import DateRange
from rentals.booking.domain.errors.invalid_nightly_rate import InvalidNightlyRate


class BookingPriceCalculator:
    DISCOUNT_THRESHOLD_DAYS = 7
    DISCOUNT_PERCENT = 10

    @staticmethod
    def calculate_total_cents(date_range: DateRange, nightly_rate_cents: int) -> int:
        if nightly_rate_cents <= 0:
            raise InvalidNightlyRate()

        days = date_range.days()
        total = days * nightly_rate_cents

        if days >= BookingPricingService.DISCOUNT_THRESHOLD_DAYS:
            discount = (total * BookingPricingService.DISCOUNT_PERCENT) // 100
            total = total - discount

        return total
```

---

## 🐍 Conceptos de Python introducidos en este capítulo

### Constantes de clase

* `DISCOUNT_THRESHOLD_DAYS` y `DISCOUNT_PERCENT` viven en la clase porque son reglas “fijas” del negocio (por ahora).

---

### `@staticmethod`

Se usa cuando:

* el método no depende del estado interno del objeto
* representa una operación del dominio

---

### Enteros como dinero (por qué usamos `*_cents`)

En este curso representamos dinero como **enteros en céntimos**:

* 1000 = 10,00€

Esto evita errores de precisión con decimales.

Más adelante, quizás, podremos introducir un Value Object `Money`.

---

## 🧠 Qué hemos aprendido

* Un Domain Service contiene reglas de negocio que no tienen dueño natural
* El ejemplo de “precio” encaja mejor que el de “solapamiento”
* El Domain Service es dominio puro: sin DB, sin HTTP, sin framework

---

## ✅ Check final

Antes de continuar deberías poder explicar:

* qué es un Domain Service
* por qué el cálculo de precio no lo ponemos en `DateRange`
* por qué evitamos meterlo en `Booking`
* cómo se lanza un error de dominio desde un Domain Service