with cities as (
   select * from {{ ref('stg_world_db__cities') }}
),

rank_per_population_cities as (
   select
      city_id,
      city,
      country_code,
      city_district_name,
      city_population,
      dense_rank() over (partition by country_code order by city_population desc) as city_population_rank_in_country
   from cities
)

select * from rank_per_population_cities