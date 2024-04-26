with source as (
    select * from {{ source('world_db', 'country_language') }}
),

reformatted as (
    select
        country_code,
        language as country_language,
        is_official as country_language_is_official,
        percentage as country_language_percentage_usage
    from source
)

select * from reformatted
