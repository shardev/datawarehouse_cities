with source as (
    select * from {{ source('country_api', 'country_api__country_locations') }}
),

country_locations as (
    select
        name as country,
        iso2 as country_iso2_code,
        long as country_longitude,
        lat as country_latitude
    from source
)

select * from country_locations