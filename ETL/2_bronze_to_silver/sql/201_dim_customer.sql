-- Insert data into silver.dim_customer from bronze.kna1, keeping only the latest operation per client.

INSERT INTO silver.dim_customer (
    cod_cliente,
    nombre_cliente,
    pais,
    ciudad,
    tipo_cliente,
    telefono
)
SELECT
    kunnr AS cod_cliente,
    name1 AS nombre_cliente,
    land1 AS pais,
    ort01 AS ciudad,
    ktokd AS tipo_cliente,
    telf1 AS telefono
FROM (
    SELECT
        v.*,
        ROW_NUMBER() OVER (
            PARTITION BY mandt, kunnr
            ORDER BY
                CASE operation_flag
                    WHEN 'L' THEN 1
                    WHEN 'U' THEN 2
                    WHEN 'I' THEN 3
                    ELSE 4
                END
        ) AS rn
    FROM bronze.kna1 v
) t
WHERE rn = 1
  AND mandt = '800'
  AND kunnr IS NOT NULL
ON CONFLICT (cod_cliente)
DO UPDATE SET
    nombre_cliente = EXCLUDED.nombre_cliente,
    pais = EXCLUDED.pais,
    ciudad = EXCLUDED.ciudad,
    tipo_cliente = EXCLUDED.tipo_cliente,
    telefono = EXCLUDED.telefono;