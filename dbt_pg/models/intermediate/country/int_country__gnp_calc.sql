with countries_has_higher_gnp_counter as (
    select 
        country_code,
        country,
        continent,
        country_gross_national_product,
        (row_number() over (order by country_gross_national_product desc) - 1) as num_of_countries_has_higher_gnp,
        percent_rank() over (order by country_gross_national_product) AS country_gnp_percentile	
    from {{ ref('stg_world_db__countries') }}
),

countries_highest_gnp_per_continent as (
    select country_code, country_highest_gnp_per_continent, continent from ( 
        select 
            country_code,
            country as country_highest_gnp_per_continent,
            continent,
            (row_number() over (partition by continent order by country_gross_national_product desc) - 1) as num
        from {{ ref('stg_world_db__countries') }}
    ) where num = 0
),

final as (
    select 
        chhgc.country_code,
        chhgc.country,
        chgpc.continent,
        chhgc.country_gross_national_product,
        chhgc.num_of_countries_has_higher_gnp,
        chhgc.country_gnp_percentile,
        chgpc.country_highest_gnp_per_continent
    from countries_has_higher_gnp_counter chhgc 
    left join countries_highest_gnp_per_continent chgpc on chhgc.continent = chgpc.continent
)

select * from final
