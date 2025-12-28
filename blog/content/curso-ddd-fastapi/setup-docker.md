---
title: "Capítulo 1.1 – Setup profesional desde cero con Docker"
weight: 1
---

## Qué vas a aprender

En este capítulo vas a aprender:

* Por qué **no instalar nada** en tu ordenador es una buena decisión
* Qué es Docker y para qué lo usamos en este curso
* Cómo montar un entorno profesional desde cero
* Cómo arrancar una API real sin conocer Python
* Cómo trabajar de forma cómoda usando `make`

> Objetivo final del capítulo: tener una API funcionando en tu máquina sin ensuciar tu sistema.

---

## Problema

Cuando empiezas a programar, es muy fácil encontrarte con problemas como:

* Tener que instalar muchas cosas en tu ordenador
* Versiones incompatibles de herramientas
* Que algo funcione “en mi máquina” pero no en otra
* No saber qué puedes borrar y qué no

Esto genera frustración y hace que aprender sea más difícil de lo necesario.

---

## Idea clave

> **El entorno de desarrollo no debe ser un problema.**

Por eso vamos a usar **Docker** desde el primer día.

Docker nos permite crear un entorno aislado donde:

* Python ya viene instalado
* Las librerías están controladas
* El proyecto funciona igual hoy y dentro de un año

---

## ¿Qué es Docker? (explicado fácil)

Docker es una herramienta que permite crear **contenedores**.

Un contenedor es como una **caja aislada** donde:

* se instala Python
* se instalan las librerías
* se ejecuta la aplicación

Tu ordenador **no se ensucia** y, si algo va mal, basta con borrar el contenedor.

> Piensa en Docker como una pequeña máquina virtual, pero ligera y específica para una aplicación.

---

## Estructura del proyecto

Después de este primer paso, el proyecto tiene esta estructura:

```
ddd-fastapi-rentals/
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .dockerignore
│
├── setup/
│   ├── requirements.txt
│   └── requirements-dev.txt
│
├── src/
│   └── rentals/
│       ├── domain/
│       ├── application/
│       ├── infrastructure/
│       └── interfaces/
│
├── tests/
├── main.py
└── Makefile
```

Esta estructura separa claramente:

* infraestructura
* código de negocio
* configuración

---

## Implementación en el proyecto

### Directorio `docker/`

Aquí vive todo lo relacionado con Docker. Esto nos permite cambiar la infraestructura sin tocar el código.

#### `Dockerfile`

Describe cómo se construye el contenedor:

```
FROM python:3.11-slim
```

Usamos una imagen oficial y ligera de Python.

---

```
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
```

Evita archivos innecesarios y mejora los logs.

---

```
WORKDIR /app
```

Define el directorio de trabajo dentro del contenedor.

---

```
RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential \
  && rm -rf /var/lib/apt/lists/*
```

Instala dependencias básicas del sistema.

---

```
COPY setup/requirements.txt setup/requirements-dev.txt /app/
```

Copia las dependencias del proyecto.

---

```
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt
```

Instala las librerías.

---

```
COPY . /app
```

Copia el código del proyecto.

---

```
EXPOSE 8000
```

Expone el puerto de la aplicación.

---

```
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

Arranca el servidor web.

---

### `docker-compose.yml`

Define cómo se ejecuta el contenedor:

* puerto
* volúmenes
* variables de entorno

---

### Makefile

El `Makefile` simplifica el trabajo diario:

```
make up    # levanta el proyecto
make down  # lo para
make logs  # muestra logs
```

---

## Check final

Antes de seguir, deberías poder decir:

* [ ] Docker arranca sin errores
* [ ] Puedo acceder a `http://localhost:8000/health`
* [ ] Veo la documentación en `http://localhost:8000/docs`
* [ ] Entiendo qué problema resuelve Docker

---

## Ejercicios

1. Cambia el título de la API en `main.py` y recarga el navegador.
2. Cambia el puerto `8000` por `8001` y comprueba que sigue funcionando.
3. Para el contenedor y vuelve a levantarlo usando solo `make`.

---

## Errores típicos

* **Dockerfile not found** → el `docker-compose.yml` apunta a una ruta incorrecta.
* **Port already in use** → otro proceso usa el puerto 8000.
* **Cambios no se reflejan** → revisa el volumen en `docker-compose.yml`.

---

## Glosario rápido

* **Imagen**: plantilla a partir de la cual se crean contenedores.
* **Contenedor**: instancia en ejecución de una imagen.
* **Dockerfile**: receta para crear una imagen.
* **docker-compose**: herramienta para orquestar contenedores.

---

## Próximo capítulo

En el **Capítulo 02** dejaremos Docker a un lado y empezaremos con lo importante:

> **pensar el dominio antes de escribir código**.

Continuamos en **02 — Dominio: pensar antes de programar** 🚀
