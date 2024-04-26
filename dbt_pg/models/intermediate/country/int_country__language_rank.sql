with countries_official_language as (
    select 
        country_code, 
        country_language as country_official_language 
    from {{ ref('stg_world_db__country_languages') }}
    where country_language_is_official = true
),

countries_popularity_language as (
    select 
        country_code,
        string_agg(country_language || ':' || country_language_percentage_usage, ',' order by country_language_percentage_usage desc) as country_languages_stringify
    from {{ ref('stg_world_db__country_languages') }}
    group by country_code
),

final as (
    select 
        cpl.country_code,
        cof.country_official_language,
        cpl.country_languages_stringify
    from countries_popularity_language cpl
    left join countries_official_language cof on cpl.country_code = cof.country_code
)

select * from final