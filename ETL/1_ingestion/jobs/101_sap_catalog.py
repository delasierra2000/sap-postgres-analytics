# -----------------------------------------------
# Dependencies
# -----------------------------------------------
from datetime import datetime
from pathlib import Path
from common.db_connection import connect__postgres, get_database_url
from common.db_load import read_csv_table, replace_load


# -----------------------------------------------
# Project Roots
# -----------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_URL = get_database_url()
CSV_PATH = str(PROJECT_ROOT / "Sample_data")

# -----------------------------------------------
# Main Execution
# -----------------------------------------------
if __name__ == "__main__":
    try:
        if not DB_URL:
            raise ValueError(
                "Database URL is required. Set LINK_POSTGREE_DB."
            )

        conn = connect__postgres(DB_URL)

        # Tables and columns to load into Supabase PostgreSQL
        LOAD_TABLE = [
            ["kna1", ["mandt", "kunnr", "name1", "land1", "ort01", "stceg", "ktokd", "telf1", "operation_flag"]],
            ["vbak", ["mandt", "vbeln", "erdat", "kunnr", "vkorg", "vtweg", "spart", "netwr", "waerk", "audat", "bstnk", "operation_flag"]],
            ["vbap", ["mandt", "vbeln", "posnr", "matnr", "netpr", "kwmeng", "vrkme", "meins", "abgru", "operation_flag"]],
            ["vbrk", ["mandt", "vbeln", "fkdat", "kunag", "netwr", "waerk", "fkart", "bukrs", "vbtyp", "operation_flag"]],
            ["vbrp", ["mandt", "vbeln", "posnr", "matnr", "fkimg", "vrkme", "netwr", "meins", "aubel", "aupos", "operation_flag"]],
            ["mara", ["mandt", "matnr", "mtart", "mbrsh", "matkl", "meins", "ersda", "operation_flag"]],
            ["vbpa", ["mandt", "vbeln", "posnr", "parvw", "kunnr", "operation_flag"]],
            ["t001w", ["mandt", "werks", "name1", "land1", "operation_flag"]],
            ["makt", ["mandt", "matnr", "spras", "maktx", "operation_flag"]]
            ]

        # Iterate over each table and load data into Supabase PostgreSQL
        for table_name, columns_to_keep in LOAD_TABLE:

            # Initialize batch ID to recognize the current load batch
            batch_id = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Construct the CSV file path for the current table
            CSV_FILE_PATH = CSV_PATH + "/" + table_name + ".csv"
            headers, rows = read_csv_table(CSV_FILE_PATH, columns_to_keep)

            # Load data into Supabase PostgreSQL
            replace_load(
                conn,
                schema="bronze",
                table_name=table_name,
                columns=["batch_id", "source_system", *headers],
                rows=rows,
                batch_id=batch_id,
                source_system="SAP",
            )
            print(f"table_name: {table_name} loaded successfully")
    except Exception as error:
        print("Proceso fallo")
        print(error)
