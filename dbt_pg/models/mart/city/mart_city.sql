with mart_city as (
    select 
        int_cities.city_id,
        int_cities.city,
        int_cities.country_code,
        int_cities.city_district_name,
        int_cities.city_population,
        int_cities.city_population_rank_in_country,

        stg_contries.country,
        stg_contries.continent,
        stg_contries.country_surface_area,
        stg_contries.country_indep_year,
        stg_contries.country_population,
        stg_contries.country_government_form,
        stg_contries.country_capital,

        int_country_gnp.country_gross_national_product,
        int_country_gnp.num_of_countries_has_higher_gnp,
        int_country_gnp.country_gnp_percentile,
        int_country_gnp.country_highest_gnp_per_continent,

        int_country_life_exp.country_life_expectancy,
        int_country_life_exp.country_life_expectancy_rank_in_world,	
        int_country_life_exp.country_life_expectancy_rank_per_continent,

        int_country_language.country_official_language,
        int_country_language.country_languages_stringify    

    from {{ ref('int_city__rank_per_population') }} as int_cities
    left join {{ ref('stg_world_db__countries') }} as stg_contries on int_cities.country_code = stg_contries.country_code
    left join {{ ref('int_country__gnp_calc') }} as int_country_gnp on int_cities.country_code = int_country_gnp.country_code
    left join {{ ref('int_country__rank_per_life_expectancy') }} as int_country_life_exp on int_cities.country_code = int_country_life_exp.country_code
    left join {{ ref('int_country__language_rank') }} as int_country_language on int_cities.country_code = int_country_language.country_code
)

select * from mart_city
