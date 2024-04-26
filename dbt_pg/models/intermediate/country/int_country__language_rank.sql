with countries_official_language as (
    select 
        country_code, 
        country,
        language as official_language 
    from public.country_language
    where is_official = true
),

countries_popularity_language as (
    select 
        country_code,
        string_agg(language || ':' || percentage, ',' order by percentage desc) as country_languages_stringify
    from public.country_language
    group by country_code
),

final as (
    select 
        cpl.country_code,
        cof.country,
        cof.official_language,
        cpl.country_languages_stringify
    from countries_popularity_language cpl
    left join countries_official_language cof on cof.country_code
)

select * from final
