.PHONY: help setup setup-env setup-dbt-profile up down restart logs clean

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

setup: setup-env setup-dbt-profile ## Setup the project environment and dbt profiles
	@echo "Setup complete! Please start the services with 'make up'."
	@echo "After services start, don't forget to setup Airflow connections as described in setup-project.md."

setup-env: ## Create .env file with default configurations if it doesn't exist
	@if [ ! -f .env ]; then \
		echo "Creating .env file..."; \
		echo "# --- ClickHouse & Storage Config ---" > .env; \
		echo "CHVER=latest" >> .env; \
		echo "" >> .env; \
		echo "# --- Airflow Core Config ---" >> .env; \
		echo "AIRFLOW_UID=50000" >> .env; \
		echo "_AIRFLOW_WWW_USER_USERNAME=airflow" >> .env; \
		echo "_AIRFLOW_WWW_USER_PASSWORD=airflow" >> .env; \
		echo "AIRFLOW__API_AUTH__JWT_SECRET=airflow_jwt_secret" >> .env; \
		echo "" >> .env; \
		echo "# --- Database Credentials (Postgres for Airflow) ---" >> .env; \
		echo "POSTGRES_USER=airflow" >> .env; \
		echo "POSTGRES_PASSWORD=airflow" >> .env; \
		echo "POSTGRES_DB=airflow" >> .env; \
		echo "" >> .env; \
		echo "# --- MinIO Credentials ---" >> .env; \
		echo "MINIO_ROOT_USER=minio" >> .env; \
		echo "MINIO_ROOT_PASSWORD=minio123" >> .env; \
		echo "" >> .env; \
		echo "# --- ClickHouse Credentials ---" >> .env; \
		echo "CLICKHOUSE_USER=default" >> .env; \
		echo "CLICKHOUSE_PASSWORD=" >> .env; \
		echo ".env file created."; \
	else \
		echo ".env file already exists, skipping creation."; \
	fi

setup-dbt-profile: ## Create dbt/profiles.yml if it doesn't exist
	@if [ ! -f dbt/profiles.yml ]; then \
		echo "Creating dbt/profiles.yml..."; \
		mkdir -p dbt; \
		echo "streamify:" > dbt/profiles.yml; \
		echo "  target: local" >> dbt/profiles.yml; \
		echo "" >> dbt/profiles.yml; \
		echo "  outputs:" >> dbt/profiles.yml; \
		echo "" >> dbt/profiles.yml; \
		echo "    local:" >> dbt/profiles.yml; \
		echo "      type: clickhouse" >> dbt/profiles.yml; \
		echo "      host: localhost" >> dbt/profiles.yml; \
		echo "      port: 8123" >> dbt/profiles.yml; \
		echo "      user: default" >> dbt/profiles.yml; \
		echo "      password: \"\"" >> dbt/profiles.yml; \
		echo "      schema: streamify_databases" >> dbt/profiles.yml; \
		echo "      secure: false" >> dbt/profiles.yml; \
		echo "" >> dbt/profiles.yml; \
		echo "    docker:" >> dbt/profiles.yml; \
		echo "      type: clickhouse" >> dbt/profiles.yml; \
		echo "      host: clickhouse" >> dbt/profiles.yml; \
		echo "      port: 8123" >> dbt/profiles.yml; \
		echo "      user: default" >> dbt/profiles.yml; \
		echo "      password: \"\"" >> dbt/profiles.yml; \
		echo "      schema: streamify_databases" >> dbt/profiles.yml; \
		echo "      secure: false" >> dbt/profiles.yml; \
		echo "dbt/profiles.yml created."; \
	else \
		echo "dbt/profiles.yml already exists, skipping creation."; \
	fi

up: ## Start all services in detached mode
	docker compose up -d

down: ## Stop all services
	docker compose down

restart: down up ## Restart all services

logs: ## Tail logs for all services
	docker compose logs -f

clean: ## Remove services, volumes, and temporary configuration files
	docker compose down -v
