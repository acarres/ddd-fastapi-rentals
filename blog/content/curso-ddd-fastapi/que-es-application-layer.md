---

title: "Application Layer: qué es y qué no es"
weight: 5
----------

# 3.1 — Application Layer: qué es y qué no es

## 🧭 Bloque 3 — Application Layer

> En este capítulo introducimos una de las capas más mal entendidas del software.
> La **Application Layer** no contiene reglas de negocio, pero sin ella el sistema no funciona.

---

## 🎯 Qué vas a aprender

En este capítulo vas a aprender:

* Qué es la **Application Layer** en DDD
* Qué problema resuelve
* Qué responsabilidades tiene
* Qué NO debe hacer nunca
* Cómo se relaciona con el dominio

> Objetivo del capítulo: saber **dónde poner cada cosa** y evitar sistemas caóticos.

---

## 🧠 El problema típico sin Application Layer

Cuando empezamos a programar, solemos hacer esto:

* lógica en controladores
* validaciones en la API
* reglas repartidas por el código
* llamadas directas a la base de datos

El resultado es:

* código difícil de entender
* reglas duplicadas
* cambios peligrosos
* tests imposibles

Este problema **no es de Python**.
Es de **arquitectura**.

---

## 💡 Idea clave

> **La Application Layer orquesta, el dominio decide.**

La Application Layer:

* coordina acciones
* ejecuta casos de uso
* conecta capas

Pero **no toma decisiones de negocio**.

---

## 🧩 Qué es la Application Layer (DDD)

Desde DDD, la Application Layer es la capa que:

* recibe una intención del exterior
* ejecuta un caso de uso
* coordina entidades y repositorios
* devuelve un resultado

Ejemplos de intenciones:

* crear una reserva
* cancelar una reserva
* cambiar una fecha

---

## ❌ Qué NO es la Application Layer

La Application Layer **NO es**:

* el dominio
* la API
* la infraestructura
* una capa de validaciones técnicas

Y **NO debe**:

* contener reglas de negocio
* conocer SQL
* conocer FastAPI
* modificar directamente la base de datos

---

## 🧠 Conceptos DDD introducidos

### Caso de uso

Un **caso de uso** es una acción completa que el sistema ofrece.

Ejemplos:

* CrearBooking
* CancelBooking

Un caso de uso:

* tiene un objetivo claro
* se ejecuta de principio a fin
* usa el dominio

---

## 🐍 Conceptos de Python introducidos

### Clases de servicio

En Python usamos **clases** para representar casos de uso.

No son entidades.
No tienen estado propio.

---

### Métodos públicos

El método principal de un caso de uso suele llamarse:

* `execute`
* `handle`
* `__call__`

---

## 🧱 Aplicación al proyecto

La Application Layer vive aquí:

```
src/rentals/booking/application/
```

Aquí pondremos:

* casos de uso
* orquestación
* coordinación entre capas

---

## 📄 Ejemplo conceptual

Imagina el caso de uso **Crear una reserva**.

La Application Layer:

1. recibe la intención
2. crea una entidad `Booking`
3. la guarda usando un repositorio
4. devuelve el resultado

La lógica de fechas **no está aquí**.

---

## 🚨 Error típico

Poner esto en Application Layer:

* `if start_date > end_date`

Eso es dominio.

---

## ✔️ Check final

Antes de continuar, deberías poder decir:

* [ ] Entiendo qué es la Application Layer
* [ ] Sé qué responsabilidades tiene
* [ ] Sé qué cosas NO deben ir aquí
* [ ] Entiendo la diferencia entre dominio y aplicación

---
