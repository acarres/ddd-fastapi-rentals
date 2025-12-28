PROJECT_NAME=ddd-fastapi-rentals
COMPOSE_FILE=docker/docker-compose.yml
SERVICE=api

.PHONY: up down restart logs

up:
	docker compose -f $(COMPOSE_FILE) up --build

down:
	docker compose -f $(COMPOSE_FILE) down

restart: down up

logs:
	docker compose -f $(COMPOSE_FILE) logs -f

test:
	docker compose -f $(COMPOSE_FILE) exec $(SERVICE) pytest

test-file:
	docker compose -f $(COMPOSE_FILE) exec $(SERVICE) pytest $(f)

test-k:
	docker compose -f $(COMPOSE_FILE) exec $(SERVICE) pytest -k "$(k)"

test-path:
	docker compose -f $(COMPOSE_FILE) exec $(SERVICE) pytest $(p)