with source as (
    select * from {{ source('world_db', 'city') }}
),

reformatted as (
    select
        id as city_id,
        name as city,
        country_code,
        district as city_district_name,
        population as city_population
    from source
)

select * from reformatted