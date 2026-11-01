import csv
from io import StringIO
from pathlib import Path
from typing import Iterable, Sequence

import psycopg


def run_sql_file(conn: psycopg.Connection, sql_path: str | Path) -> None:
    """Execute a full SQL script using the provided connection.

    Args:
        conn: Active PostgreSQL connection.
        sql_path: Path to the SQL file.
    """
    sql_file = Path(sql_path)
    print(f"Running SQL file: {sql_file}")
    if not sql_file.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_file}")

    sql_text = sql_file.read_text(encoding="utf-8").strip()
    print("mirando SQL file content:")
    print(sql_text)
    if not sql_text:
        return

    with conn.cursor() as cur:
        # Run script as-is to support DO blocks and internal semicolons.
        cur.execute(sql_text, prepare=False)


def read_csv_table(
    csv_path: str,
    columns_to_keep: Sequence[str] | None = None,
    encoding: str = "utf-8-sig",
) -> tuple[list[str], list[list[str]]]:
    """Read a CSV file into memory as (columns, rows).

    Args:
        csv_path: CSV file path.
        columns_to_keep: Optional subset of column names to keep.
        encoding: CSV file encoding. Defaults to utf-8-sig.

    Returns:
        A tuple with the selected columns and the corresponding row values.
    """
    with open(csv_path, "r", encoding=encoding, newline="") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        if not header:
            return [], []

        selected_columns = list(header) if columns_to_keep is None else [
            col for col in columns_to_keep if col in header
        ]

        rows: list[list[str]] = []
        for row in reader:
            rows.append([row.get(col, "") for col in selected_columns])

        return selected_columns, rows


def truncate_table(
    conn: psycopg.Connection,
    schema: str,
    table_name: str,
    where_clause: str | None = None,
    commit: bool = True,
) -> None:
    """Delete all rows from a table or a filtered subset.

    Args:
        conn: Active PostgreSQL connection.
        schema: Target schema name.
        table_name: Name of the target table.
        where_clause: Optional SQL condition such as "source_system = %s".
        commit: Whether to commit immediately.
    """
    sql = f"delete from {schema}.{table_name}"
    if where_clause:
        sql = f"{sql} where {where_clause}"

    with conn.cursor() as cur:
        cur.execute(sql)
    if commit:
        conn.commit()


def copy_rows_to_table(
    conn: psycopg.Connection,
    schema: str,
    table_name: str,
    columns: Sequence[str],
    rows: Iterable[Sequence[str]],
    commit: bool = True,
    batch_id: str | None = None,
    source_system: str | None = None,
) -> None:
    """Load rows into a PostgreSQL table using COPY FROM STDIN.

    Args:
        conn: Active PostgreSQL connection.
        schema: Target schema name.
        table_name: Name of the target table.
        columns: Column list in the target table.
        rows: Iterable of row values to insert.
        commit: Whether to commit immediately.
        batch_id: Optional batch identifier added before each row when target columns
            start with batch_id and source_system.
        source_system: Optional source system name added alongside the batch_id.
    """
    if not columns:
        raise ValueError("columns cannot be empty")

    normalized_rows = list(rows)
    if (
        batch_id is not None
        and source_system is not None
        and len(columns) >= 2
        and columns[0] == "batch_id"
        and columns[1] == "source_system"
    ):
        normalized_rows = [
            [batch_id, source_system, *row]
            for row in normalized_rows
        ]

    column_sql = ", ".join(columns)
    copy_sql = (
        f"copy {schema}.{table_name} ({column_sql}) "
        "from stdin with (format csv, header false, null '')"
    )

    buffer = StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerows(normalized_rows)
    buffer.seek(0)

    with conn.cursor() as cur:
        with cur.copy(copy_sql) as copy:
            copy.write(buffer.getvalue())
    if commit:
        conn.commit()


def replace_load(
    conn: psycopg.Connection,
    schema: str,
    table_name: str,
    columns: Sequence[str],
    rows: Iterable[Sequence[str]],
    where_clause: str | None = None,
    batch_id: str | None = None,
    source_system: str | None = None,
) -> None:
    """Delete the target rows and replace them with the provided data in a transaction.

    This is a safe full-load pattern: if anything fails during the replace process,
    the transaction is rolled back and the previous table state remains intact.

    Args:
        conn: Active PostgreSQL connection.
        schema: Target schema name.
        table_name: Target table name.
        columns: Column list in the target table.
        rows: Iterable row values to be inserted after the delete.
        where_clause: Optional SQL filter for the delete operation, e.g. "source_system = %s".
        batch_id: Optional batch identifier pushed into each row when target columns include
            batch_id and source_system.
        source_system: Optional source system added alongside batch_id.
    """
    original_autocommit = conn.autocommit
    try:
        conn.autocommit = False

        sql = f"delete from {schema}.{table_name}"
        if where_clause:
            sql = f"{sql} where {where_clause}"

        with conn.cursor() as cur:
            cur.execute(sql)

        copy_rows_to_table(
            conn,
            schema,
            table_name,
            columns,
            rows,
            commit=False,
            batch_id=batch_id,
            source_system=source_system,
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.autocommit = original_autocommit
