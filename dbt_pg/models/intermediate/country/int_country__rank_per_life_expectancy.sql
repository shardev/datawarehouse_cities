-- todo
select 
	country_code,
	country,
	continent,
	country_surface_area,
	country_indep_year,
	country_population,
	country_life_expectancy,
	case
		when country_life_expectancy is not null then
			dense_rank() over (order by country_life_expectancy desc) 
		else null
	end as country_life_exp_rank_in_world,
	
	country_gross_national_product,
	country_government_form,
	country_capital
from