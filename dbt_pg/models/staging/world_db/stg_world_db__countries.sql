with source as (
    select * from {{ source('world_db', 'country') }}
),

reformatted as (
    select
        code as country_code,
        name as country,
        continent,
        surface_area as country_surface_area,
        indep_year as country_indep_year,
        population as country_population,
        life_expectancy as country_life_expectancy,
        gnp as country_gross_national_product,
        government_form as country_government_form,
        capital as country_capital
    from source
)

select * from reformatted
