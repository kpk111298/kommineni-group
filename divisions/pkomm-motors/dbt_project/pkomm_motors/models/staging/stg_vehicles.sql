-- ============================================================
-- Silver Layer: stg_vehicles
-- ============================================================

WITH source AS (

    SELECT * FROM {{ source('bronze', 'vehicles') }}

),

cleaned AS (

    SELECT
        vehicle_id,
        -- Title case, except short brand names like BMW that are written in capitals
        CASE
            WHEN LENGTH(TRIM(make)) <= 3 THEN UPPER(TRIM(make))
            ELSE CONCAT(UPPER(SUBSTR(TRIM(make), 1, 1)), LOWER(SUBSTR(TRIM(make), 2)))
        END AS make,
        CONCAT(UPPER(SUBSTR(model, 1, 1)), LOWER(SUBSTR(model, 2))) AS model,
        CAST(year AS INTEGER) AS year,
        ROUND(list_price, 2) AS list_price,
        LOWER(status) AS status,
        location_id,

        -- Flag premium vehicles (above 50k)
        CASE
            WHEN list_price > 50000 THEN TRUE
            ELSE FALSE
        END AS is_premium,

        _ingested_at,
        _source_file

    FROM source

    -- Only keep valid vehicles
    WHERE vehicle_id IS NOT NULL
    AND list_price > 0
    AND year >= 2020

)

SELECT * FROM cleaned