---

title: "Setup profesional desde cero con Docker"
weight: 1
---------

# 1.1 — Setup profesional desde cero con Docker

## 🧱 Bloque 1 — Fundamentos y entorno

> En este capítulo vamos a preparar **el entorno de trabajo** sobre el que construiremos todo el curso.
> No vamos a aprender Python todavía.
> Vamos a asegurarnos de que **el entorno no sea un problema**.

---

> 🔍 **Sobre el “Check final”**
> Al final de cada capítulo encontrarás un **Check final**.
> No es un examen ni algo que tengas que entregar.
> Es una lista de verificación para que compruebes si has entendido lo mínimo necesario para continuar.
>
> Si no puedes marcar todos los puntos, no pasa nada: vuelve a leer el capítulo con calma antes de seguir.

---

## 🎯 Qué vas a aprender

En este capítulo vas a aprender:

* Por qué **no instalar nada** en tu ordenador es una buena decisión
* Qué es Docker y para qué lo usamos en este curso
* Cómo montar un entorno profesional desde cero
* Cómo arrancar una API real sin conocer Python
* Cómo trabajar de forma cómoda usando `make`

> **Objetivo final del capítulo**: tener una API funcionando en tu máquina **sin ensuciar tu sistema**.

---

## 🧠 El problema real al empezar a programar

Cuando empiezas a programar, es muy fácil encontrarte con problemas como:

* Tener que instalar muchas cosas en tu ordenador
* Versiones incompatibles de herramientas
* Que algo funcione “en mi máquina” pero no en otra
* No saber qué puedes borrar y qué no

Esto genera frustración y hace que aprender sea **mucho más difícil de lo necesario**.

---

## 💡 Idea clave

> **El entorno de desarrollo no debe ser un problema.**

Por eso vamos a usar **Docker** desde el primer día.

Docker nos permite crear un entorno aislado donde:

* Python ya viene instalado
* Las librerías están controladas
* El proyecto funciona igual hoy y dentro de un año

---

## 🐳 ¿Qué es Docker? (explicado fácil)

Docker es una herramienta que permite crear **contenedores**.

Un contenedor es como una **caja aislada** donde:

* se instala Python
* se instalan las librerías
* se ejecuta la aplicación

Tu ordenador **no se ensucia** y, si algo va mal, basta con borrar el contenedor.

> Piensa en Docker como una pequeña máquina virtual, pero ligera y específica para una aplicación.

---

## 🧱 Estructura del proyecto

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

## 🐳 Docker en el proyecto

### 📁 Directorio `docker/`

Aquí vive todo lo relacionado con Docker. Esto nos permite cambiar la infraestructura **sin tocar el código**.

---

## 📄 `docker/Dockerfile`

El `Dockerfile` describe **cómo se construye la imagen** del contenedor.

### Imagen base

```dockerfile
FROM python:3.11-slim
```

Usamos una imagen oficial y ligera de Python.

---

### Variables de entorno

```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
```

Evita archivos innecesarios y mejora los logs.

---

### Directorio de trabajo

```dockerfile
WORKDIR /app
```

Define el directorio de trabajo dentro del contenedor.

---

### Dependencias del sistema

```dockerfile
RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential \
  && rm -rf /var/lib/apt/lists/*
```

Instala herramientas básicas del sistema.

---

### Dependencias de Python

```dockerfile
COPY setup/requirements.txt setup/requirements-dev.txt /app/
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt
```

---

### Código del proyecto

```dockerfile
COPY . /app
```

---

### Puerto y comando de arranque

```dockerfile
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

---

### ✅ Dockerfile final

```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential \
  && rm -rf /var/lib/apt/lists/*

COPY setup/requirements.txt setup/requirements-dev.txt /app/
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

---

## 📄 `docker/docker-compose.yml`

```yaml
services:
  api:
    build:
      context: ..
      dockerfile: docker/Dockerfile

    ports:
      - "8000:8000"

    volumes:
      - ..:/app

    environment:
      - PYTHONPATH=/app/src
```

---

## 🛠️ Makefile

### 📄 Archivo `Makefile`

```makefile
COMPOSE_FILE=docker/docker-compose.yml

.PHONY: up down logs restart

up:
	docker compose -f $(COMPOSE_FILE) up --build

down:
	docker compose -f $(COMPOSE_FILE) down

logs:
	docker compose -f $(COMPOSE_FILE) logs -f

restart: down up
```

---

### 🧠 ¿Qué es un Makefile?

Un **Makefile** define atajos de comandos para trabajar más cómodo. No es Python ni forma parte del dominio.

---

### ▶️ Comandos disponibles

* `make up` → levanta el proyecto
* `make down` → para el proyecto
* `make logs` → muestra logs
* `make restart` → reinicia todo

---

## ✔️ Check final

Antes de continuar con el curso, deberías poder decir:

* [ ] Sé explicar con mis propias palabras qué es Docker
* [ ] Entiendo por qué no instalamos Python en mi ordenador
* [ ] Sé qué diferencia hay entre `Dockerfile` y `docker-compose.yml`
* [ ] Soy capaz de arrancar y parar el proyecto usando `make`
* [ ] Puedo acceder a la API y a la documentación en el navegador

---

## 🧪 Ejercicios

1. Cambia el título de la API en `main.py` y recarga el navegador.
2. Cambia el puerto `8000` por `8001` y comprueba que sigue funcionando.
3. Para el contenedor y vuelve a levantarlo usando solo `make`.

---

## ❌ Errores típicos

* **Dockerfile not found** → ruta incorrecta en `docker-compose.yml`
* **Port already in use** → otro proceso usa el puerto 8000
* **Cambios no se reflejan** → revisa el volumen

---

## 📘 Glosario rápido

* **Imagen**: plantilla para crear contenedores
* **Contenedor**: instancia en ejecución de una imagen
* **Dockerfile**: receta para crear una imagen
* **docker-compose**: orquestador de contenedores

---

## 🔜 Próximo capítulo

En el **Capítulo 2.1** empezaremos con lo importante:

> **pensar el dominio antes de escribir código**
