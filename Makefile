SHELL := /usr/bin/bash

.PHONY: up down build logs ps restart clean pull

up:
	docker compose up -d
	echo "Stack is starting. Visit: Homer http://localhost:8080, Grafana http://localhost:3000, Prometheus http://localhost:9090, Dozzle http://localhost:9999, Portainer http://localhost:9000, Node-RED http://localhost:1880, Task Service http://localhost:8000/docs"

down:
	docker compose down

build:
	docker compose build

pull:
	docker compose pull

logs:
	docker compose logs -f

ps:
	docker compose ps

restart:
	docker compose restart

clean:
	docker compose down -v