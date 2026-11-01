# Repository Review and Portfolio Plan

Date: 2026-11-01
Project: supabase-lab
Objective: make this repository portfolio-ready to showcase ETL engineering and reporting capabilities.

## Executive Summary

This repository has a strong conceptual base for a layered ETL (bronze to silver) and business reporting use case inspired by SAP sales data. The biggest blockers are reproducibility and trust signals for reviewers: committed secrets, broken bootstrap path for empty PostgreSQL, schema/model inconsistencies, and minimal root documentation/tests.

If these are fixed, the project can become a strong portfolio piece with:
- deterministic setup from empty database,
- clear pipeline orchestration,
- quality checks and test evidence,
- reporting outputs linked to business questions.

## What Was Reviewed

- ETL scripts and SQL assets in ETL/1_ingestion and ETL/2_bronze_to_silver.
- Shared DB utilities in common.
- Project metadata and dependencies.
- Documentation and onboarding files.
- Tests and repository hygiene.

## Findings (Prioritized)

### 1) Critical: Plaintext database credentials committed in source code

Evidence:
- ETL/1_ingestion/10_create_schema_tables.py (DB_URL hardcoded)
- ETL/1_ingestion/11_sap_catalog.py (DB_URL hardcoded)
- ETL/2_bronze_to_silver/20_dimpliente.py (DB_URL hardcoded)

Risk:
- security exposure,
- poor engineering signal in portfolio review,
- unsafe for collaboration and CI.

Required fix:
- use environment variables only (DATABASE_URL and/or SUPABASE_DB_URL),
- remove credentials from Git history if possible.

---

### 2) Critical: Empty-database bootstrap currently fails due to missing SQL file reference

Evidence:
- ETL/1_ingestion/10_create_schema_tables.py points to sql/01_create_tables.sql
- actual existing file is ETL/1_ingestion/sql/10_create_tables.sql

Risk:
- first run on empty PostgreSQL fails,
- repository is not reproducible.

Required fix:
- align SQL_PATH with real file,
- add one canonical bootstrap command that always works from clean DB.

---

### 3) Critical: Column contract mismatch between ingestion, bronze schema, and silver transform

Evidence:
- Ingestion mapping for vbrk uses kunag in ETL/1_ingestion/11_sap_catalog.py
- Bronze vbrk DDL defines kunnr in ETL/1_ingestion/sql/10_create_tables.sql
- Silver fact SQL selects kunag from bronze.vbrk in ETL/2_bronze_to_silver/sql/20_dim_cliente.sql

Risk:
- load/runtime failures,
- inconsistent business semantics,
- untrusted reporting results.

Required fix:
- define and enforce one canonical customer key column contract end-to-end.

---

### 4) High: Silver table creation is separated from transform execution

Evidence:
- ETL/2_bronze_to_silver/20_dimpliente.py executes only 20_dim_cliente.sql
- silver DDL is in ETL/2_bronze_to_silver/sql/20_create_tables.sql

Risk:
- transforms fail unless manual pre-step is run,
- brittle onboarding.

Required fix:
- include silver DDL in bootstrap sequence (idempotent) before DML transforms.

---

### 5) High: Portfolio documentation is too thin at root and tests are missing

Evidence:
- README.md currently contains only "hola"
- tests directory exists but is empty

Risk:
- reviewers cannot quickly understand architecture,
- no proof of reliability or quality.

Required fix:
- full root README with architecture, runbook, expected outputs,
- add smoke/unit/integration test scaffolding.

---

### 6) Medium: SQL asset duplication and ambiguity

Evidence:
- ETL/1_ingestion/sql/10_create_tables.sql
- ETL/1_ingestion/sql/create_tables copy.sql
- ETL/1_ingestion/sql/alter_tables.sql is empty

Risk:
- uncertainty about authoritative schema,
- maintenance drift.

Required fix:
- keep one canonical DDL per stage,
- remove or archive deprecated SQL files clearly.

---

### 7) Medium: SQL runner prints full SQL text to logs

Evidence:
- common/db_load.py prints entire SQL contents before execution.

Risk:
- noisy logs,
- potential leakage of sensitive SQL/procedural logic in shared logs.

Required fix:
- log filename and execution status, not full SQL body by default.

## Structural Critique (Portfolio Perspective)

### Strengths

- Clear medallion intent (bronze to silver).
- Practical SAP-inspired dataset and business-oriented reporting topic.
- Reusable utility modules for DB connection and load mechanics.
- SQL-first transformations are good for analytics engineering portfolios.

### Weaknesses

- No single deterministic bootstrap workflow from zero.
- Inconsistent naming/contracts between scripts and DDL.
- No orchestration layer implemented yet (you selected Dagster or Airflow direction).
- Missing test and quality guardrails.
- Missing polished storytelling (README, diagrams, output evidence).

## Target State for Portfolio Quality

A reviewer should be able to:
1. Clone repository.
2. Configure environment variables.
3. Run one bootstrap command against empty PostgreSQL.
4. Execute ETL (bronze load + silver transforms) through orchestrator.
5. Run data quality checks.
6. Open reporting SQL and dashboard evidence.

All in a predictable, documented flow.

## Implementation Plan

### Phase 1: Security + Bootstrap Reliability (P0)

1. Remove all hardcoded DB URLs and read only from environment.
2. Fix ingestion schema SQL path mismatch.
3. Create one ordered bootstrap runner:
   - bronze schema/tables,
   - silver schema/tables,
   - optional seed/reference data.
4. Make all bootstrap SQL idempotent.

Deliverable:
- clean first-run setup from empty PostgreSQL.

---

### Phase 2: Data Contract Consistency (P0)

1. Standardize customer key fields across bronze and silver (kunnr vs kunag decision).
2. Update ingestion mapping and transform SQL to match canonical contract.
3. Add schema comments/data dictionary for key business fields.

Deliverable:
- consistent model and reliable transformations.

---

### Phase 3: Repository Organization (P1)

1. Define canonical SQL naming convention (example: 010_, 020_, 030_).
2. Remove duplicate/obsolete SQL files.
3. Add stage-level README files in ETL folders:
   - purpose,
   - inputs,
   - outputs,
   - run commands.

Deliverable:
- clean and navigable project structure.

---

### Phase 4: Orchestration (P1)

Chosen direction: Dagster or Airflow.

1. Implement pipeline DAG/assets with explicit dependencies:
   - bootstrap -> bronze ingest -> silver transforms -> reporting marts.
2. Add local run instructions and dependency graph screenshot/export.
3. Add retry/failure behavior and basic logging strategy.

Deliverable:
- production-like orchestration story for portfolio.

---

### Phase 5: Data Quality and Testing (P1)

1. Add data quality checks:
   - key not null,
   - duplicate key checks,
   - row count sanity checks.
2. Add tests:
   - unit tests for utility functions,
   - smoke tests for SQL file existence/order,
   - integration test scaffold for end-to-end run.

Deliverable:
- objective quality and reliability evidence.

---

### Phase 6: Reporting Showcase (P1)

Chosen artifact direction: BI dashboard docs/exports.

1. Add curated KPI/mart SQL for:
   - sales by customer,
   - sales by product,
   - monthly billing,
   - order vs invoice,
   - geo distribution.
2. Document metric definitions and assumptions.
3. Add dashboard evidence package in Documentation:
   - screenshots,
   - model mapping,
   - source query references.

Deliverable:
- visible business impact and reporting outcomes.

---

### Phase 7: Portfolio Storytelling + CI (P2)

1. Replace root README with complete project narrative:
   - architecture diagram,
   - quickstart,
   - command sequence,
   - sample outputs,
   - known limitations and roadmap.
2. Add CI workflow:
   - lint/tests,
   - bootstrap integrity check,
   - ETL smoke check.

Deliverable:
- reviewer-friendly and professional presentation.

## Proposed Structure (Reference)

This is a suggested target structure for readability and execution:

- ETL/
  - bootstrap/
    - 010_create_bronze.sql
    - 020_create_silver.sql
    - run_bootstrap.py
  - ingestion/
    - run_bronze_ingestion.py
    - sql/
  - transforms/
    - run_silver_transforms.py
    - sql/
  - quality/
    - run_quality_checks.py
    - sql/
- orchestration/
  - dagster_or_airflow_project/
- reporting/
  - marts/
  - kpis/
- Documentation/
  - architecture.md
  - quickstart.md
  - dashboard_evidence.md

## Verification Checklist

- Bootstrap runs successfully on empty PostgreSQL.
- Re-running bootstrap is idempotent.
- Bronze load completes without schema mismatch.
- Silver transforms complete without column contract errors.
- Data quality checks pass for baseline sample data.
- README quickstart works for a clean clone.

## Effort and Priority

- P0 (immediate): security + bootstrap + contract consistency.
- P1 (next): orchestration + quality checks + reporting evidence.
- P2 (polish): CI and full portfolio narrative optimization.

## Notes Captured During Review

- Environment setup guide already exists and is useful as a baseline.
- Packaging with pyproject.toml and editable install is a good foundation.
- Current docs on SAP-inspired reports are a strong business context and should be linked directly from README once the pipeline is stabilized.

## Final Recommendation

Prioritize P0 fixes before adding new features. Once setup is deterministic and secure, implement orchestration and reporting evidence quickly. This sequence maximizes portfolio impact and reviewer confidence.
