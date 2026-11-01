-- Bootstrap deploy script for an empty PostgreSQL database.
-- Creates all schemas and tables needed by the ETL pipeline.

CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;

-- =========================
-- Bronze layer tables
-- =========================

-- 1) Cliente
CREATE TABLE IF NOT EXISTS bronze.kna1 (
    batch_id TEXT,
    source_system TEXT,
    mandt VARCHAR(3),
    kunnr VARCHAR(20),
    name1 VARCHAR(255),
    land1 VARCHAR(10),
    ort01 VARCHAR(120),
    stceg VARCHAR(30),
    ktokd VARCHAR(10),
    telf1 VARCHAR(30),
    operation_flag VARCHAR(2)
);

-- 2) Cabecera de pedido
CREATE TABLE IF NOT EXISTS bronze.vbak (
    batch_id TEXT,
    source_system TEXT,
    mandt VARCHAR(3),
    vbeln VARCHAR(20),
    erdat VARCHAR(20),
    kunnr VARCHAR(20),
    vkorg VARCHAR(20),
    vtweg VARCHAR(20),
    spart VARCHAR(20),
    netwr NUMERIC(18,2),
    waerk VARCHAR(10),
    audat VARCHAR(20),
    bstnk VARCHAR(40),
    operation_flag VARCHAR(2)
);

-- 3) Posicion de pedido
CREATE TABLE IF NOT EXISTS bronze.vbap (
    batch_id TEXT,
    source_system TEXT,
    mandt VARCHAR(3),
    vbeln VARCHAR(20),
    posnr VARCHAR(20),
    matnr VARCHAR(40),
    netpr NUMERIC(18,2),
    kwmeng NUMERIC(18,3),
    vrkme VARCHAR(10),
    meins VARCHAR(10),
    abgru VARCHAR(10),
    operation_flag VARCHAR(2)
);

-- 4) Cabecera de factura
CREATE TABLE IF NOT EXISTS bronze.vbrk (
    batch_id TEXT,
    source_system TEXT,
    mandt VARCHAR(3),
    vbeln VARCHAR(20),
    fkdat VARCHAR(20),
    kunag VARCHAR(20),
    netwr NUMERIC(18,2),
    waerk VARCHAR(10),
    fkart VARCHAR(10),
    bukrs VARCHAR(10),
    vbtyp VARCHAR(10),
    operation_flag VARCHAR(2)
);

-- 5) Posicion de factura
CREATE TABLE IF NOT EXISTS bronze.vbrp (
    batch_id TEXT,
    source_system TEXT,
    mandt VARCHAR(3),
    vbeln VARCHAR(20),
    posnr VARCHAR(20),
    matnr VARCHAR(40),
    fkimg NUMERIC(18,3),
    vrkme VARCHAR(10),
    netwr NUMERIC(18,2),
    meins VARCHAR(10),
    aubel VARCHAR(20),
    aupos VARCHAR(20),
    operation_flag VARCHAR(2)
);

-- 6) Maestro de materiales
CREATE TABLE IF NOT EXISTS bronze.mara (
    batch_id TEXT,
    source_system TEXT,
    mandt VARCHAR(3),
    matnr VARCHAR(40),
    mtart VARCHAR(10),
    mbrsh VARCHAR(10),
    matkl VARCHAR(20),
    meins VARCHAR(10),
    ersda VARCHAR(20),
    operation_flag VARCHAR(2)
);

-- 7) Partners
CREATE TABLE IF NOT EXISTS bronze.vbpa (
    batch_id TEXT,
    source_system TEXT,
    mandt VARCHAR(3),
    vbeln VARCHAR(20),
    posnr VARCHAR(20),
    parvw VARCHAR(10),
    kunnr VARCHAR(20),
    operation_flag VARCHAR(2)
);

-- 8) Almacen
CREATE TABLE IF NOT EXISTS bronze.t001w (
    batch_id TEXT,
    source_system TEXT,
    mandt VARCHAR(3),
    werks VARCHAR(20),
    name1 VARCHAR(255),
    land1 VARCHAR(10),
    operation_flag VARCHAR(2)
);

-- 9) Texto producto
CREATE TABLE IF NOT EXISTS bronze.makt (
    batch_id TEXT,
    source_system TEXT,
    mandt VARCHAR(3),
    matnr VARCHAR(40),
    spras VARCHAR(10),
    maktx VARCHAR(255),
    operation_flag VARCHAR(2)
);

-- =========================
-- Silver layer tables
-- =========================

CREATE TABLE IF NOT EXISTS silver.dim_customer (
    cod_cliente VARCHAR(20) NOT NULL,
    nombre_cliente VARCHAR(255),
    pais VARCHAR(10),
    ciudad VARCHAR(120),
    tipo_cliente VARCHAR(10),
    telefono VARCHAR(30),
    CONSTRAINT pk_dim_customer PRIMARY KEY (cod_cliente)
);

CREATE TABLE IF NOT EXISTS silver.fact_billing_doc (
    numero_factura VARCHAR(20) NOT NULL,
    fecha_factura DATE,
    cliente_id VARCHAR(20),
    importe_factura NUMERIC(18,2),
    moneda VARCHAR(10),
    tipo_factura VARCHAR(10),
    sociedad VARCHAR(10),
    tipo_documento VARCHAR(10),
    PRIMARY KEY (numero_factura)
);

CREATE TABLE IF NOT EXISTS silver.fact_billing_doc_pos (
    numero_factura VARCHAR(20) NOT NULL,
    posicion_factura VARCHAR(20) NOT NULL,
    material_id VARCHAR(40),
    cantidad_facturada NUMERIC(18,3),
    unidad_cantidad VARCHAR(10),
    importe_neto NUMERIC(18,2),
    unidad_precio VARCHAR(10),
    documento_origen VARCHAR(20),
    posicion_origen VARCHAR(20),
    PRIMARY KEY (numero_factura, posicion_factura)
);
