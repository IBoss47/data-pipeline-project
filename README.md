# Data Engineering Platform

This is a comprehensive Data Engineering Platform template that integrates **Apache Airflow**, **dbt**, **ClickHouse**, and **MinIO**. It is fully containerized using Docker Compose for easy local development, testing, and deployment.

## 🏗 Architecture & Core Services

The platform consists of the following core components working together:

* **Apache Airflow** (Orchestration): Workflow management platform for data pipeline scheduling and monitoring. Configured with `CeleryExecutor` for scalable task execution.
  * **PostgreSQL**: Metadata database for Airflow.
  * **Redis**: Message broker for Airflow's Celery workers.
* **dbt** (Transformation): Data Build Tool for transforming data in the warehouse. It is mounted into Airflow so DAGs can trigger dbt runs.
* **ClickHouse** (Data Warehouse): Extremely fast open-source OLAP database for analytical queries.
  * **ClickHouse Keeper**: Coordination system for ClickHouse data replication (Raft consensus).
* **MinIO** (Data Lake / Object Storage): S3-compatible object storage server for raw data and artifacts.

---

## 📂 Project Structure

```text
de-platform/
├── .env                  # Environment variables configuration
├── airflow/              # Airflow workspace (DAGs, plugins, custom config)
│   ├── dags/             # Put your Airflow DAGs here
│   ├── plugins/          # Custom Airflow plugins
│   └── Dockerfile        # Custom Airflow image build definition
├── data/                 # Local data directory (mounted to ClickHouse & Airflow)
├── dbt/                  # dbt project directory (models, macros, tests)
├── docker-compose.yaml   # Main Docker Compose configuration
├── fs/                   # Configuration files for ClickHouse and Keeper
├── scripts/              # Initialization scripts (e.g., ClickHouse init-db.sh)
├── services/             # Additional custom services or scripts
└── sql/                  # SQL scripts and queries
```

---

## 🚀 Setup & Installation

### Prerequisites
* **Docker** and **Docker Compose** installed on your machine.
* At least **4GB of RAM** allocated to Docker (8GB+ recommended).

### 1. Configure Environment Variables
The repository comes with a default `.env` file. To ensure Airflow works correctly with local file permissions (especially on Linux/macOS), it is highly recommended to set your local user ID in the `.env` file:

```bash
echo -e "AIRFLOW_UID=$(id -u)" >> .env
```

### 2. Start the Platform
Run the following command to initialize and start all services in the background:

```bash
docker compose up -d
```

*(Note: The first time you run this, Docker will build the custom Airflow image and download other necessary images, which might take a few minutes. The `airflow-init` service will also run automatically to prepare the Airflow metadata database and create the default admin user.)*

### 3. Verify the Setup
Check if all containers are running successfully:
```bash
docker compose ps
```
Look for `Up (healthy)` status on core services like `airflow-webserver`, `clickhouse`, and `minio`.

---

## 🌐 Accessing UIs and Services

Once everything is up and running, you can access the following web interfaces from your browser:

| Service | URL | Default Credentials (User / Pass) |
|---------|-----|-----------------------------------|
| **Apache Airflow** | [http://localhost:8080](http://localhost:8080) | `airflow` / `airflow` |
| **MinIO Console** | [http://localhost:9001](http://localhost:9001) | `minio` / `minio123` |
| **ClickHouse Play UI** | [http://localhost:8123/play](http://localhost:8123/play) | *No auth required* |

*(Note: Flower can be enabled via Docker Compose profiles if you need to monitor Celery workers at port 5555).*

---

## 🔌 Database Connections

### Connecting to ClickHouse
You can connect to ClickHouse using any SQL client (like DBeaver or DataGrip) or via the built-in CLI.

**Using clickhouse-client (CLI):**
```bash
# Enter interactive shell
docker exec -it clickhouse clickhouse-client

# Run a single query
docker exec -it clickhouse clickhouse-client --query "SELECT version()"
```

**Using DBeaver / DataGrip:**
* **Host**: `127.0.0.1`
* **Port**: `8123` (HTTP) or `9000` (Native TCP)
* **Username**: `default`
* **Password**: *(leave blank)*

### Connecting to MinIO (S3 API)
When writing scripts (Python, boto3, etc.) to interact with MinIO, use these credentials:
* **API Endpoint**: `http://127.0.0.1:9000`
* **Access Key**: `minio`
* **Secret Key**: `minio123`

---

## 🧹 Managing the Platform

**Stop all services (keeps data intact):**
```bash
docker compose down
```

**Restart the platform:**
```bash
docker compose restart
```

**Completely reset the environment (⚠️ Deletes all databases and data volumes):**
```bash
docker compose down -v
```

## 🛠 Adding Python Packages to Airflow

If you need to add custom Python packages to Airflow:
1. Update the `airflow/Dockerfile` or add a `requirements.txt`.
2. Rebuild the Airflow image by running:
```bash
docker compose build airflow-apiserver
docker compose up -d
```
*(Alternatively, for quick checks, you can use the `_PIP_ADDITIONAL_REQUIREMENTS` variable in `.env`)*
