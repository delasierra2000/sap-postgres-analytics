import os
from pathlib import Path

import psycopg

## Database connection utilities for PostgreSQL using psycopg.


def load_local_env(env_file: Path | None = None) -> None:
    """Load key/value pairs from a local .env file into os.environ.

    Existing environment variables are not overwritten.
    """
    project_root = Path(__file__).resolve().parents[1]
    env_path = env_file or project_root / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


def get_database_url() -> str | None:
    """Resolve database URL from common environment variable names.

    Currently, only LINK_POSTGREE_DB is considered.
    """
    load_local_env()
    return (
        os.getenv("LINK_POSTGREE_DB")
    )

def connect__postgres(db_url: str) -> psycopg.Connection:
    """Open a direct PostgreSQL connection using the provided DB URL.

    Args:
        db_url (str): The PostgreSQL connection URL.

    Returns:
        psycopg.Connection: An active PostgreSQL connection.
    """
    return psycopg.connect(db_url, autocommit=False)


def test_connect_postgres(conninfo: str, timeout_seconds: int = 8) -> tuple[bool, str]:
    """Check whether the given PostgreSQL URL is reachable.

    Args:
        conninfo (str): The PostgreSQL connection URL.
        timeout_seconds (int, optional): Connection timeout in seconds. Defaults to 8.

    Returns:
        tuple[bool, str]: A tuple where the first element indicates success, and the second element contains a message.
    """
    try:
        with psycopg.connect(conninfo, connect_timeout=timeout_seconds, autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute("select 1")
                cur.fetchone()
        return True, "ok"
    except Exception as error:
        return False, str(error)
