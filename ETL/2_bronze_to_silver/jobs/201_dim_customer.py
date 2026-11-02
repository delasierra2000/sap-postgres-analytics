from pathlib import Path
from common.db_connection import connect__postgres, get_database_url
from common.db_load import run_sql_file

STAGE_ROOT = Path(__file__).resolve().parents[1]

DB_URL = get_database_url()

# SQL file with silver table definitions for dim_customer.
SQL_PATH = STAGE_ROOT / "sql" / "201_dim_customer.sql"


def main() -> None:
    if not DB_URL:
        raise ValueError(
            "Database URL is required. Set LINK_POSTGREE_DB."
        )

    conn = connect__postgres(DB_URL)
    try:
        run_sql_file(conn, SQL_PATH)
        conn.commit()
        print("Data loaded into silver.dim_customer successfully")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
