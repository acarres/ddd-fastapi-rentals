PROJECT_NAME=ddd-fastapi-rentals
COMPOSE_FILE=docker/docker-compose.yml

.PHONY: up down restart logs

up:
	docker compose -f $(COMPOSE_FILE) up --build

down:
	docker compose -f $(COMPOSE_FILE) down

restart: down up

logs:
	docker compose -f $(COMPOSE_FILE) logs -f