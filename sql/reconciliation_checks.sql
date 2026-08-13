/*
  Illustrative reconciliation checks for an SAP HANA source extract and a
  Microsoft Fabric target table. Adapt schema names and SQL dialect details
  to the governed environments. This repository does not make live connections.
*/

-- 1. Row counts
SELECT 'HANA_SOURCE' AS dataset, COUNT(*) AS row_count
FROM staging.hana_orders
UNION ALL
SELECT 'FABRIC_TARGET' AS dataset, COUNT(*) AS row_count
FROM curated.fabric_orders;

-- 2. Duplicate business-key detection (run against each dataset)
SELECT order_id, COUNT(*) AS occurrence_count
FROM staging.hana_orders
GROUP BY order_id
HAVING COUNT(*) > 1;

SELECT order_id, COUNT(*) AS occurrence_count
FROM curated.fabric_orders
GROUP BY order_id
HAVING COUNT(*) > 1;

-- 3. Null or required-field checks (repeat for the target table)
SELECT order_id
FROM staging.hana_orders
WHERE order_id IS NULL
   OR customer_id IS NULL
   OR product IS NULL
   OR quantity IS NULL
   OR unit_price IS NULL
   OR order_date IS NULL
   OR status IS NULL;

SELECT order_id
FROM curated.fabric_orders
WHERE order_id IS NULL
   OR customer_id IS NULL
   OR product IS NULL
   OR quantity IS NULL
   OR unit_price IS NULL
   OR order_date IS NULL
   OR status IS NULL;

-- 4. Aggregate reconciliation by order date
WITH source_totals AS (
    SELECT order_date,
           COUNT(*) AS order_count,
           SUM(quantity) AS total_quantity,
           SUM(quantity * unit_price) AS total_order_value
    FROM staging.hana_orders
    GROUP BY order_date
),
target_totals AS (
    SELECT order_date,
           COUNT(*) AS order_count,
           SUM(quantity) AS total_quantity,
           SUM(quantity * unit_price) AS total_order_value
    FROM curated.fabric_orders
    GROUP BY order_date
)
SELECT s.order_date,
       s.order_count AS source_order_count,
       t.order_count AS target_order_count,
       s.total_quantity AS source_quantity,
       t.total_quantity AS target_quantity,
       s.total_order_value AS source_value,
       t.total_order_value AS target_value
FROM source_totals s
FULL OUTER JOIN target_totals t ON s.order_date = t.order_date
WHERE COALESCE(s.order_count, -1) <> COALESCE(t.order_count, -1)
   OR COALESCE(s.total_quantity, -1) <> COALESCE(t.total_quantity, -1)
   OR COALESCE(s.total_order_value, -1) <> COALESCE(t.total_order_value, -1);

-- 5. Business-status distribution
SELECT 'HANA_SOURCE' AS dataset, status, COUNT(*) AS order_count
FROM staging.hana_orders
GROUP BY status
UNION ALL
SELECT 'FABRIC_TARGET' AS dataset, status, COUNT(*) AS order_count
FROM curated.fabric_orders
GROUP BY status
ORDER BY status, dataset;
