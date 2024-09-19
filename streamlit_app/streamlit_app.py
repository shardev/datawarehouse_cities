import streamlit as st
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium


# Database connection
def get_connection():
    return psycopg2.connect(
        dbname="pg_db",
        user="admin",
        password="root",
        host="postgres"  # Name of the postgres service from docker-compose
    )

# 1: Fetch top 10 cities based on population with continent filter
def fetch_top_cities(continent):
    query = """
    SELECT city, country, city_population
    FROM mart_city 
    WHERE continent = %s
    ORDER BY city_population DESC
    LIMIT 10;
    """
    conn = get_connection()
    df = pd.read_sql(query, conn, params=(continent,))
    conn.close()
    return df

# 2: Fetch country populations based on continent
def fetch_country_population(continent):
    query = """
        SELECT distinct country, country_population
        FROM mart_city
        WHERE continent = %s
        ORDER BY country_population DESC
        LIMIT 5;
    """
    conn = get_connection()
    df = pd.read_sql(query, conn, params=(continent,))
    conn.close()
    return df

# 3: Youngest and oldest established country in continent
def youngest_oldest_country(continent):
    query = """
        SELECT 
            CASE 
                WHEN MIN(country_indep_year) < 0 THEN CONCAT('BC ', CAST(ABS(MIN(country_indep_year)) as VARCHAR(100)))
                ELSE CAST(MIN(country_indep_year) AS VARCHAR(100))
            END AS country_indep_year_min_format,
            CASE 
                WHEN MAX(country_indep_year) < 0 THEN CONCAT('BC ', CAST(ABS(MAX(country_indep_year)) as VARCHAR(100)))
                ELSE CAST(MAX(country_indep_year) AS VARCHAR(100))
            END AS country_indep_year_max_format
        FROM mart_city
        WHERE continent = %s  
    """
    conn = get_connection()
    df = pd.read_sql(query, conn, params=(continent,))
    conn.close()
    return df

# 4: Worst n GDP performing countries in continent => list countries with higest num_of_countries_has_higher_gdp
def fetch_gnp_data(continent):
    query = """
    SELECT 
        country,
        country_gross_national_product,
        AVG(country_gross_national_product) OVER (PARTITION BY continent) AS avg_gnp
    FROM int_country__gnp_calc
    WHERE continent = %s
    ORDER BY num_of_countries_has_higher_gnp ASC
    LIMIT 10
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, (continent,))
    rows = cur.fetchall()
    conn.close()

    # Convert to DataFrame
    df = pd.DataFrame(rows, columns=['country', 'gnp', 'avg_gnp'])
    return df

# 5:  Show 5 countries per continent with highest and 5 with lowest life expectancy
def high_low_country_life_expectancy(continent):
    query = """
    (SELECT DISTINCT
        country,
        country_life_expectancy_rank_per_continent,
        country_life_expectancy,
        'HIGH' AS country_order
    FROM mart_city
	WHERE continent = %s
	ORDER BY country_life_expectancy_rank_per_continent ASC
	LIMIT 5
    )
    UNION ALL
    (SELECT DISTINCT
        country,
        country_life_expectancy_rank_per_continent,
        country_life_expectancy,
        'LOW' AS country_order
    FROM mart_city
    WHERE continent = %s
    ORDER BY country_life_expectancy_rank_per_continent DESC
    LIMIT 5
    )
    """
    conn = get_connection()
    df = pd.read_sql(query, conn, params=(continent, continent))
    conn.close()
    return df

# 6: Try to show on global map dots for each country and when hovered to display which country it is
def countries_geodata(continent):
    query = """
    SELECT 
        l.country,
        l.country_iso2_code,
        l.country_longitude,
        l.country_latitude,
        co.continent,
        co.country_surface_area,
        co.country_population
    FROM stg_country_api__country_locations l
    INNER JOIN stg_world_db__countries co ON l.country = co.country
    WHERE co.continent = %s
    """

    conn = get_connection()
    df = pd.read_sql(query, conn, params=(continent,))
    conn.close()
    return df

# Function to fetch distinct countries based on a selected continent
def get_countries_by_continent(continent):
    query = """
    SELECT DISTINCT
        country
    FROM mart_city
    WHERE continent = %s
    """

    conn = get_connection()
    df = pd.read_sql(query, conn, params=(continent,))
    conn.close()
    return df['country'].tolist()

# 7: Get cities by country
def get_cities_by_country(country):
    query = """
    SELECT 
        city,
        country_code as "country code",
        country,
        continent,
        city_population as "city population",
        city_population_rank_in_country as "size order of a city inside country"
    FROM mart_city
    WHERE country = %s
    """

    conn = get_connection()
    df = pd.read_sql(query, conn, params=(country,))
    conn.close()
    return df

# 8: Get languages by country
def get_languages_by_country(country):
    query = """
    SELECT 
        l.country_code, 
        co.country,
        l.country_official_language, 
        l.country_languages_stringify
    FROM int_country__language_rank l
    INNER JOIN stg_world_db__countries co on l.country_code = co.country_code
    WHERE country = %s
    """
    
    conn = get_connection()
    df = pd.read_sql(query, conn, params=(country,))
    official_language = df['country_official_language'].iloc[0]
    split_languages = df['country_languages_stringify'].iloc[0]
    conn.close()
    
    return (official_language, split_languages)

# 9: Get country gnp description
def get_country_gnp_description(country):
    query = """
    SELECT 
        country_code,
        country,
        continent,
        country_gross_national_product,
        num_of_countries_has_higher_gnp,
        country_gnp_percentile,
        country_highest_gnp_per_continent
    FROM int_country__gnp_calc
    WHERE country = %s
    """

    conn = get_connection()
    df = pd.read_sql(query, conn, params=(country,))
    conn.close()
    return (df['country_gross_national_product'].iloc[0], df['num_of_countries_has_higher_gnp'].iloc[0], df['country_gnp_percentile'].iloc[0] , df['country_highest_gnp_per_continent'].iloc[0])


# ---------------------------
# Streamlit app
# ---------------------------
st.title("World geography analysis dashboard")

# Continent filter
continent = st.selectbox('Select Continent', ['Asia', 'Europe', 'Africa', 'North America', 'South America', 'Oceania', 'Antarctica'])

st.header("Continent based analysis:", divider=True)
    
# Fetch and display data
if continent:
    # 6
    # GeoMap: Center map around the first country in the list
    country_data = countries_geodata(continent)
    first_country = country_data.iloc[0, :]
    m = folium.Map(location=[first_country['country_latitude'], first_country['country_longitude']], zoom_start=3, width='100%')

    # Add a marker for each country in the selected continent
    for country in country_data.itertuples():
        folium.Marker(
            [country.country_latitude, country.country_longitude],
            popup=f"{country.country} ({country.country_iso2_code}), Country surface area: {country.country_surface_area} km2, Country population: {country.country_population/ 1_000_000:.2f}M", 
            tooltip=f"{country.country}",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

    st_data = st_folium(m, width=1000, height=750)

    # 2
    # Calculate total population and country percentages
    countries_population = fetch_country_population(continent)
    total_population = countries_population['country_population'].sum()
    countries_population['percentage'] = (countries_population['country_population'] / total_population) * 100

    st.write(f"Total population of {continent}: {total_population:,}")

    # Display the pie chart
    fig, ax = plt.subplots()
    ax.pie(countries_population['country_population'], labels=countries_population['country'], autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    ax.axis('equal')  # Equal aspect ratio ensures that the pie chart is circular.
    st.pyplot(fig)
    st.write("Population breakdown by 5 largest countries:")
    st.dataframe(countries_population[['country', 'country_population', 'percentage']])

    # 1
    top_cities_per_continent = fetch_top_cities(continent)
    st.write(f"Top 10 biggest cities in {continent}:")
    st.dataframe(top_cities_per_continent)

    # 3
    st.subheader("Youngest and oldest country in continent:", divider = False)
    youngest_oldest_c = youngest_oldest_country(continent)
    years = youngest_oldest_c.iloc[0,:]
    
    min_year = int(years[0].replace('BC ', '-')) if 'BC' in years[0] else int(years[0])
    max_year = int(years[1].replace('BC ', '-')) if 'BC' in years[1] else int(years[1])

    fig, ax = plt.subplots(figsize=(10, 2))
    ax.plot([min_year, max_year], [0, 0], 'o-', color='b')
    ax.annotate(years[0], (min_year, 0), textcoords="offset points", xytext=(-10, 10), ha='center')
    ax.annotate(years[1], (max_year, 0), textcoords="offset points", xytext=(-10, 10), ha='center')

    ax.set_xlim(min(min_year - 50, -3000), max(max_year + 50, 2023))  # Add buffer to the limits
    ax.get_yaxis().set_visible(False)
    ax.spines[["left", "top", "right"]].set_visible(False)

    st.pyplot(fig)

    # 4
    st.subheader("Top 10 Countries by GNP with Avg GNP Line:", divider = False)
    highest_gnp = fetch_gnp_data(continent)
    countries = highest_gnp['country']
    gnp_values = highest_gnp['gnp']
    avg_gnp_value = highest_gnp['avg_gnp'].iloc[0]  
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(countries, gnp_values, color='skyblue', label='GNP per Country')
    ax.axhline(y=avg_gnp_value, color='r', linestyle='--', label=f'Avg continent GNP: {avg_gnp_value:.2f}')
    ax.set_xlabel('Country')
    ax.set_ylabel('Gross National Product (GNP)')
    ax.set_title('Top 10 Countries by GNP with Avg GNP Line')
    plt.xticks(rotation=45, ha='right')

    ax.legend()
    st.pyplot(fig)


    # 5 
    high_low_exp = high_low_country_life_expectancy(continent)
    st.subheader(f"Top 5 and Bottom 5 Countries in {continent} by Life Expectancy:", divider = False)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    # Separate the top 5 (HIGH) and bottom 5 (LOW)
    high = high_low_exp[high_low_exp['country_order'] == 'HIGH']
    low = high_low_exp[high_low_exp['country_order'] == 'LOW']

    ax.bar(high['country'], high['country_life_expectancy'], color='green', label='High Life Expectancy')
    ax.bar(low['country'], low['country_life_expectancy'], color='red', label='Low Life Expectancy')
    ax.set_xlabel('Country')
    ax.set_ylabel('Life Expectancy')
    ax.set_title(f'Life Expectancy in Top 5 and Bottom 5 Countries in {continent}')

    plt.xticks(rotation=45)
    ax.legend()
    st.pyplot(fig)

    # Fetch the distinct countries based on the selected continent
    st.header("Country based analysis:", divider=True)
    countries = get_countries_by_continent(continent)
    country = st.selectbox("Select a Country", countries)

    # 7
    cities_by_country = get_cities_by_country(country)
    st.write(f"Cities in {country}:")
    st.dataframe(cities_by_country)

    # 8
    (official_language, languages_by_country) = get_languages_by_country(country)
    
    language_data = [pair.split(":") for pair in languages_by_country.split(",")]
    # Extract the languages and the corresponding percentages
    languages = [item[0] for item in language_data]
    percentages = [float(item[1]) for item in language_data]

    st.subheader(f"Languages in {country}:", divider = False)
    st.write(f"Official language(s) in {country} is {official_language}.")
    st.write(f"Language distribtuion in {country}:")

    fig, ax = plt.subplots()
    ax.pie(percentages, labels=languages, autopct='%1.1f%%', startangle=140)
    ax.axis('equal') 
    st.pyplot(fig)

    # 9
    (gnp, num_higher, percentile, highest_per_continent) = get_country_gnp_description(country)
    st.subheader(f"GNP analysis:", divider = False)
    st.write(f"{country} has GNP of {gnp} millions $, which is less than {num_higher} countries world-wide. This puts {country} at {percentile*100} percentile.")

    fig, ax = plt.subplots()
    ax.hlines(y=0.5, xmin=0, xmax=100, color='lightgray', linewidth=5)
    ax.vlines(x=percentile*100, ymin=0.25, ymax=0.75, color='blue', linewidth=3)
    
    ax.set_xlim(0, 100)
    ax.set_xticks(range(0, 101, 10))  # Ticks at intervals of 10%
    ax.set_xlabel('Percentile (%)')
    
    ax.set_title(f'Percentile Marker: {percentile*100}%')
    ax.get_yaxis().set_visible(False)
    st.pyplot(fig)
    
    st.markdown(f"*Note: {highest_per_continent} has highest GNP in {continent}*")