from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run_step(script_path: Path) -> None:
    print(f"\n=== Running: {script_path} ===")
    subprocess.run([sys.executable, str(script_path)], check=True)
    print(f"=== OK: {script_path.name} ===")


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]

    steps = [
        project_root / "ETL" / "0_bootstrap" / "jobs" / "001_run_bootstrap.py",
        project_root / "ETL" / "1_ingestion" / "jobs" / "101_sap_catalog.py",
        project_root / "ETL" / "2_bronze_to_silver" / "jobs" / "201_dim_cliente.py",
    ]

    missing = [str(step) for step in steps if not step.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing pipeline step files:\n" + "\n".join(missing)
        )

    for step in steps:
        run_step(step)

    print("\nETL pipeline completed successfully.")


if __name__ == "__main__":
    main()
