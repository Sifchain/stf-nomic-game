.PHONY: init test format lint help all

# Function to run a command and indent its output
define run_and_indent
	@echo "\nRunning $(1)...\n"; \
	(poetry run $(1) $(2)) 2>&1 | sed 's/^/\t/';
endef

all: help

init:
	@echo 'Installing pre-commit hooks'
	git config core.hooksPath .githooks
	@echo 'Making pre-commit hook executable'
	chmod +x .githooks/pre-commit
	@echo 'Installing dependencies'
	poetry install

start:
	python -m nomic.main

start-watch:
	DEBUG=1 python -m nomic.main

reset-db:
	psql -U $(USER) -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='nomic';"
	psql -U $(USER) -d postgres -c "DROP DATABASE IF EXISTS nomic;"
	psql -U $(USER) -d postgres -c "CREATE DATABASE nomic;"
	alembic upgrade head

start-db:
	docker run -p 5432:5432 --name nomic-db -e POSTGRES_PASSWORD=$$DB_PASSWORD -d postgres

migrate-db:
	alembic upgrade head

build-docker:
	docker build -t nomic . 

run-docker:
	docker run -p 8080:8080 --env-file .env nomic

start-system:
	docker-compose up -d

stop-system:
	docker-compose down

format:
	@if [ -z "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
		echo "\nRunning black...\n"; \
		poetry run black . ; \
		echo "\nRunning isort...\n"; \
		poetry run isort . ; \
	else \
		echo "\nRunning black...\n"; \
		poetry run black $(filter-out $@,$(MAKECMDGOALS)); \
		echo "\nRunning isort...\n"; \
		poetry run isort $(filter-out $@,$(MAKECMDGOALS)); \
	fi

lint:
	@if [ -z "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
		echo "\nLinting with mypy...\n"; \
		poetry run mypy . ; \
		echo "\nLinting with ruff...\n"; \
		poetry run ruff . --fix ; \
	else \
		echo "\nLinting with mypy...\n"; \
		poetry run mypy $(filter-out $@,$(MAKECMDGOALS)); \
		echo "\nLinting with ruff...\n"; \
		poetry run ruff $(filter-out $@,$(MAKECMDGOALS)) --fix; \
	fi


help:
	@echo '----'
	@echo 'format              - run code formatters'
	@echo 'lint                - run linters'
	@echo 'init                - install pre-commit hooks and dependencies'
	@echo 'start               - start the application'
	@echo 'reset-db            - reset the database'
	@echo 'migrate-db          - migrate the database'
	@echo 'start_db            - start postgres db'
	@echo 'build-docker        - build docker image'
	@echo 'run-docker          - run docker image'
	@echo 'start-system        - start system with docker-compose'
	@echo 'stop-system         - stop system with docker-compose'