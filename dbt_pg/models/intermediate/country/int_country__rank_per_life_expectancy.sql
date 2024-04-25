with countries_life_exp_rank_in_world as (
    select 
        country_code,
        country,
        continent,
        country_life_expectancy,
        case
            when country_life_expectancy is not null then
                dense_rank() over (order by country_life_expectancy desc) 
            else null
        end as country_life_expectancy_rank_in_world,	
        case
            when country_life_expectancy is not null then
                dense_rank() over (partition by continent order by country_life_expectancy desc) 
            else null
	    end as country_life_expectancy_rank_per_continent
    from {{ ref('stg_world_db__countries') }}
)

select * from countries_life_exp_rank_in_world
