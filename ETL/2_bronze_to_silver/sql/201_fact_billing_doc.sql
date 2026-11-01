-- Insert data into silver.fact_billing_doc from bronze.vbrk, keeping only the latest operation per billing document.
INSERT INTO silver.fact_billing_doc (
    numero_factura,
    fecha_factura,
    cliente_id,
    importe_factura,
    moneda,
    tipo_factura,
    sociedad,
    tipo_documento 
)
WITH ranked AS (
    SELECT
        v.*,
        ROW_NUMBER() OVER (
            PARTITION BY mandt, vbeln
            ORDER BY
                CASE operation_flag
                    WHEN 'L' THEN 1
                    WHEN 'U' THEN 2
                    WHEN 'I' THEN 3
                    ELSE 4
                END
        ) AS rn
    FROM bronze.vbrk v
    WHERE mandt = '800'
)
SELECT
    vbeln AS numero_factura,
    CASE
        WHEN fkdat IS NULL OR trim(fkdat) = '' THEN NULL
        WHEN fkdat ~ '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' THEN TO_DATE(fkdat, 'YYYY-MM-DD')
        WHEN fkdat ~ '^[0-9]{8}$' THEN TO_DATE(fkdat, 'YYYYMMDD')
        ELSE NULL
    END AS fecha_factura,
    CASE
        WHEN kunag IS NULL OR trim(kunag) = '' THEN 'NO_INFORMADO'
        ELSE kunag
    END AS cliente_id,
    netwr AS importe_factura,
    waerk AS moneda,
    fkart AS tipo_factura,
    bukrs AS sociedad,
    vbtyp AS tipo_documento
FROM ranked
WHERE rn = 1
  AND vbeln IS NOT NULL
ON CONFLICT (numero_factura)
DO UPDATE SET
    fecha_factura = EXCLUDED.fecha_factura,
    cliente_id = EXCLUDED.cliente_id,
    importe_factura = EXCLUDED.importe_factura,
    moneda = EXCLUDED.moneda,
    tipo_factura = EXCLUDED.tipo_factura,
    sociedad = EXCLUDED.sociedad,
    tipo_documento = EXCLUDED.tipo_documento;