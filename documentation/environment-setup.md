# Environment Setup

Use these steps to set up the local Python environment for this repository on Windows.

## 1. Go to your local workspace directory

Choose any local path where you keep your projects, then move there:

```powershell
cd C:\repos
```

## 2. Clone the repository

From that directory, run:

```powershell
git clone <repository-url>
```

## 3. Open a terminal in the repository root

```powershell
cd sap-postgres-analytics
```

## 3.1 Keep the environment out of Git

This repository ignores `env_fin/`, so the virtual environment will not be uploaded to the repo as long as you keep it in the project root.

## 4. Create the virtual environment

```powershell
python -m venv env_fin
```

## 5. Activate the virtual environment

```powershell
.\env_fin\Scripts\Activate
```


## 6. Install dependencies

Install the project in editable mode so local package imports (for example `from common...`) work without custom `sys.path` hacks:

```powershell
pip install -e .
```

## 7. Confirm the environment

```powershell
python --version
pip --version
```

## 8. Configure database URL for local ETL runs

The ETL scripts now read database URL values from environment variables.
If a `.env` file exists in the repository root, it is loaded automatically.

1. Create your local `.env` from the template:

```powershell
Copy-Item .env.example .env
```

2. Open `.env` and set your PostgreSQL URL:

```env
LINK_POSTGREE_DB=postgresql://<user>:<password>@<host>/<database>?sslmode=require
```

## 9. Bootstrap database schemas and tables

Run the bootstrap script to create all required bronze and silver tables from a single SQL file:

```powershell
python ETL/0_bootstrap/jobs/run_bootstrap.py
```
