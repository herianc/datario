
{{ config(materialized='table') }}

with source AS (
    SELECT * 
    FROM {{ source ('postgres', 'brt_report')}}

),


renamed AS (
    select 
        codigo AS id,
        latitude AS lat,
        longitude AS lon,
        velocidade AS vel
    FROM
        source
    WHERE (ignicao = true) AND (linha != '0')
)


SELECT * FROM renamed

