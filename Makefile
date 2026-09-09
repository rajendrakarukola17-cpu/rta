SHELL := /bin/bash
COMPOSE_PROJECT_NAME ?= office-suite-v7
DC := docker compose
ENV_FILE := .env

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Office Suite v7.2 make targets"
	@echo ""
	@echo "Usage:"
	@echo "  make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  check-env              Verify .env exists"
	@echo "  config                 Validate docker-compose configuration"
	@echo "  up                     Start all services"
	@echo "  down                   Stop all services"
	@echo "  restart                Restart all services"
	@echo "  logs                   Tail logs"
	@echo "  ps                     Show service status"
	@echo "  health                 Run healthcheck script"
	@echo "  backend-shell          Open backend shell"
	@echo "  postgres-shell         Open PostgreSQL shell"
	@echo "  redis-shell            Open Redis CLI"
	@echo "  migrate                Run backend database migrations"
	@echo "  seed                   Seed development data"
	@echo "  backup-postgres        Run PostgreSQL backup script"
	@echo "  backup-minio           Run MinIO backup script"
	@echo "  restore-drill          Run restore drill script"
	@echo "  frontend-install       Install frontend dependencies"
	@echo "  frontend-dev           Run frontend dev server"
	@echo "  frontend-build         Build frontend for production"
	@echo "  test-backend           Run backend tests"
	@echo "  clean-docker           Remove stopped containers and dangling images"

.PHONY: check-env
check-env:
	@test -f $(ENV_FILE) || { echo "ERROR: $(ENV_FILE) not found. Copy .env.example to .env first."; exit 1; }

.PHONY: config
config: check-env
	$(DC) config

.PHONY: up
up: check-env
	$(DC) up -d

.PHONY: down
down:
	$(DC) down

.PHONY: restart
restart:
	$(DC) restart

.PHONY: logs
logs:
	$(DC) logs -f --tail=200

.PHONY: ps
ps:
	$(DC) ps

.PHONY: health
health:
	bash scripts/deploy/healthcheck.sh

.PHONY: backend-shell
backend-shell:
	$(DC) exec fastapi /bin/sh

.PHONY: postgres-shell
postgres-shell:
	$(DC) exec postgres psql -U $${POSTGRES_USER:-postgres} -d $${POSTGRES_DB:-office_suite}

.PHONY: redis-shell
redis-shell:
	$(DC) exec redis redis-cli

.PHONY: migrate
migrate:
	$(DC) exec fastapi alembic upgrade head

.PHONY: seed
seed:
	$(DC) exec fastapi python scripts/seed/seed-dev.py

.PHONY: backup-postgres
backup-postgres:
	bash scripts/backup/backup-postgres.sh

.PHONY: backup-minio
backup-minio:
	bash scripts/backup/backup-minio.sh

.PHONY: restore-drill
restore-drill:
	bash scripts/backup/restore-drill.sh

.PHONY: frontend-install
frontend-install:
	cd frontend && npm install

.PHONY: frontend-dev
frontend-dev:
	cd frontend && npm run dev

.PHONY: frontend-build
frontend-build:
	cd frontend && npm run build

.PHONY: test-backend
test-backend:
	$(DC) exec fastapi pytest -q

.PHONY: clean-docker
clean-docker:
	docker container prune -f
	docker image prune -f
