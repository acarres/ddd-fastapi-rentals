---
title: "Dominio: pensar antes de programar"
weight: 2
---

## Qué vas a aprender

En este capítulo vas a aprender:

* Qué significa realmente **dominio** en Domain-Driven Design
* Por qué el dominio es más importante que el código
* Qué problemas aparecen cuando empezamos programando sin pensar
* Cómo identificar reglas de negocio aunque no seas técnico
* Cómo usar este capítulo como base mental para todo lo que vendrá después

> Objetivo del capítulo: cambiar la forma en la que piensas un sistema **antes** de escribir una sola línea de código.

---

## Problema

Cuando alguien empieza a programar, suele hacerlo así:

1. Aprende un lenguaje
2. Aprende un framework
3. Empieza a escribir código
4. Ajusta sobre la marcha

El problema es que este enfoque provoca:

* Código difícil de entender
* Reglas repartidas por todas partes
* Cambios caros y arriesgados
* Sistemas que funcionan, pero no se entienden

Esto no es un problema de Python.
Es un problema de **cómo pensamos** el software.

---

## Idea clave

> **El software no trata de código, trata de negocio.**

El código solo es una forma de expresar reglas que ya existen en la realidad.

Si no entendemos bien esas reglas:

* el código será confuso
* los cambios serán dolorosos
* el sistema será frágil

DDD parte de una idea muy simple:

> Primero entendemos el dominio.
> Luego lo modelamos.
> Después escribimos código.

---

## ¿Qué es el dominio?

El **dominio** es el conjunto de:

* conceptos
* reglas
* decisiones
* restricciones

que existen en el mundo real y que el software debe respetar.

Ejemplos de dominios:

* alquiler de viviendas
* banca
* logística
* sanidad
* educación

El dominio **no es**:

* la base de datos
* la API
* el framework
* el lenguaje

---

## Ejemplo en la vida real

Imagina un sistema de alquiler de viviendas.

Antes de programar, ya existen reglas como:

* Un alquiler tiene una fecha de inicio y una de fin
* No se puede alquilar una vivienda si ya está ocupada
* Un contrato no puede empezar en el pasado
* Un alquiler puede estar activo, cancelado o finalizado

Estas reglas existen **aunque no haya software**.

Nuestro trabajo como desarrolladores no es inventarlas, sino **respetarlas y expresarlas correctamente**.

---

## Lenguaje Ubicuo (sin tecnicismos)

Para poder modelar bien un dominio, necesitamos hablar el mismo idioma.

Eso significa:

* Usar las mismas palabras que usa el negocio
* Evitar términos técnicos innecesarios
* Nombrar las cosas como se entienden en la realidad

Por ejemplo:

* Decimos *alquiler*, no *rental_record*
* Decimos *cancelar*, no *set_status_false*

> Cuando el código se lee como una conversación del negocio, vamos por buen camino.

---

## Qué pasa cuando ignoramos el dominio

Cuando no pensamos en dominio:

* Todo se convierte en CRUD
* Las reglas se meten en controladores
* Los cambios rompen cosas
* Nadie sabe dónde está la lógica

El sistema se vuelve:

* frágil
* difícil de testear
* imposible de evolucionar

---

## Implementación en el proyecto

En nuestro proyecto, el dominio vivirá en:

```
src/rentals/domain/
```

Ahí pondremos:

* Entidades
* Value Objects
* Reglas de negocio
* Errores de dominio

Importante:

> El dominio **no conoce** bases de datos, HTTP, ni frameworks.

Eso vendrá después.

---

## Check final

Antes de pasar al siguiente capítulo, deberías poder decir:

* [ ] Sé explicar qué es el dominio con mis propias palabras
* [ ] Entiendo por qué no empezamos programando
* [ ] Veo reglas de negocio en problemas cotidianos
* [ ] Entiendo por qué el dominio no depende del framework

---

## Ejercicios

1. Piensa en un sistema cotidiano (por ejemplo, un gimnasio o una tienda online).
2. Escribe 5 reglas que existan aunque no haya software.
3. Reescribe esas reglas sin usar palabras técnicas.

Ejemplo:

> “Un cliente no puede tener dos suscripciones activas al mismo tiempo.”

---

## Errores típicos

* Confundir dominio con base de datos
* Pensar que el dominio es solo una carpeta
* Empezar por el framework
* Modelar pensando en tablas

---

## Glosario rápido

* **Dominio**: conjunto de reglas y conceptos del negocio
* **DDD**: forma de diseñar software centrada en el dominio
* **Lenguaje Ubicuo**: vocabulario compartido entre negocio y código
