# SAP PostgreSQL Analytics

A practical ETL and analytics project for loading SAP-inspired business data into PostgreSQL and transforming it into analytics-ready datasets.

This repository is designed to showcase a medallion-style data pipeline: raw ingestion, bronze cleaning, and silver transformation logic using SQL and Python.

## Overview

The project is built around a PostgreSQL-based data warehouse workflow for SAP-related master and transactional tables, including sales, invoices, materials, and organizational data. It is structured to support local development and experimentation while remaining easy to extend with reporting, orchestration, and data-quality checks.

## Key features

- SAP-style sample data for realistic analytics scenarios
- PostgreSQL database loading and schema bootstrap
- ETL pipeline organized by stage
- Python utilities for connection and data loading
- SQL-first transforms for analytics engineering workflows
- Local setup compatible with a clean Windows development environment

## Repository structure

- `ETL/` — ingestion, bootstrap, and transformation jobs
- `common/` — shared database utilities
- `pipeline/` — orchestration entry points
- `Sample_data/` — sample CSV datasets used for local testing
- `documentation/` — setup and project notes
- `AI/` — project knowledge and agent assets
- `LICENSE` — repository license

## Quick start

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd sap-postgres-analytics
```

### 2. Create and activate a virtual environment

```powershell
python -m venv env_fin
.\env_fin\Scripts\Activate
```

### 3. Install dependencies

```powershell
pip install -e .
```

### 4. Configure the database connection

Create a local environment file from the template:

```powershell
Copy-Item .env.example .env
```

Then update `.env` with your PostgreSQL connection string:

```env
LINK_POSTGREE_DB=postgresql://<user>:<password>@<host>/<database>?sslmode=require
```

### 5. Run the bootstrap pipeline

```powershell
python ETL/0_bootstrap/jobs/run_bootstrap.py
```

## Tech stack

- Python 3.11+
- PostgreSQL
- pandas
- psycopg
- Pydantic

## Current focus

This repository currently emphasizes:

- raw-to-bronze ingestion
- schema bootstrapping
- standard SQL-based transformations
- local ETL execution for analytics use cases

## Roadmap

Planned next steps include:

- better pipeline orchestration
- data quality checks
- gold layer and KPI marts
- automated tests and CI
- reporting/dashboard artifacts

## License

This project is licensed under the MIT license. See [LICENSE](LICENSE) for details.

## Notes

This repo is intended as a portfolio-ready example of analytics engineering work with SAP-inspired business data. It is suitable for learning, demonstrations, and continued development as a data pipeline project.

