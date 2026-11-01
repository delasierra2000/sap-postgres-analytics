-- Insert data into silver.fact_billing_doc_pos from bronze.vbrp, keeping only the latest operation per billing line.

INSERT INTO silver.fact_billing_doc_pos (
    numero_factura,
    posicion_factura,
    material_id,
    cantidad_facturada,
    unidad_cantidad,
    importe_neto,
    unidad_precio,
    documento_origen,
    posicion_origen
)
WITH ranked AS (
    SELECT
        v.*,
        ROW_NUMBER() OVER (
            PARTITION BY mandt, vbeln, posnr
            ORDER BY
                CASE operation_flag
                    WHEN 'L' THEN 1
                    WHEN 'U' THEN 2
                    WHEN 'I' THEN 3
                    ELSE 4
                END
        ) AS rn
    FROM bronze.vbrp v
    WHERE mandt = '800'
)
SELECT
    vbeln AS numero_factura,
    posnr AS posicion_factura,
    matnr AS material_id,
    fkimg AS cantidad_facturada,
    COALESCE(vrkme, meins) AS unidad_cantidad,
    netwr AS importe_neto,
    COALESCE(vrkme, meins) AS unidad_precio,
    aubel AS documento_origen,
    aupos AS posicion_origen
FROM ranked
WHERE rn = 1
  AND vbeln IS NOT NULL
  AND posnr IS NOT NULL
ON CONFLICT (numero_factura, posicion_factura)
DO UPDATE SET
    material_id = EXCLUDED.material_id,
    cantidad_facturada = EXCLUDED.cantidad_facturada,
    unidad_cantidad = EXCLUDED.unidad_cantidad,
    importe_neto = EXCLUDED.importe_neto,
    unidad_precio = EXCLUDED.unidad_precio,
    documento_origen = EXCLUDED.documento_origen,
    posicion_origen = EXCLUDED.posicion_origen;
