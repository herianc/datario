
with source as (
    SELECT * 
    FROM {{ source ('postgres', 'brt_report')}}

),


renamed as (
    select 
        codigo as id,
        latitude as lat,
        longitude as lon,
        velocidade as vel
    FROM
        source
)


select * from renamed

