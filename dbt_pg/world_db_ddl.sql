BEGIN;
SET client_encoding TO 'UTF8';

CREATE TABLE IF NOT EXISTS city (
    id integer NOT NULL,
    name text NOT NULL,
    country_code character(3) NOT NULL,
    district text NOT NULL,
    population integer NOT NULL,
    local_name text NULL
);
COMMENT ON COLUMN city.local_name IS 'City local name';

COPY city (id, name, country_code, district, population, local_name)
FROM '/docker-entrypoint-initdb.d/seeds/city_utf8.csv'
DELIMITER ','
CSV HEADER;

CREATE TABLE IF NOT EXISTS country (
    code character(3) NOT NULL,
    name text NOT NULL,
    continent text NOT NULL,
    region text NOT NULL,
    surface_area real NOT NULL,
    indep_year smallint,
    population integer NOT NULL,
    life_expectancy real,
    gnp numeric(10,2),
    gnp_old numeric(10,2),
    local_name text NOT NULL,
    government_form text NOT NULL,
    head_of_state text,
    capital integer,
    code2 character(2) NOT NULL,
    CONSTRAINT country_continent_check CHECK ((((((((continent = 'Asia'::text) OR (continent = 'Europe'::text)) OR (continent = 'North America'::text)) OR (continent = 'Africa'::text)) OR (continent = 'Oceania'::text)) OR (continent = 'Antarctica'::text)) OR (continent = 'South America'::text)))
);

COMMENT ON COLUMN country.gnp IS 'GNP is Gross national product';
COMMENT ON COLUMN country.code2 IS 'Following ISO 3166-1 alpha-2 code';

COPY country (code, name, continent, region, surface_area, indep_year, population, life_expectancy, gnp, gnp_old, local_name, government_form, head_of_state, capital, code2)
FROM '/docker-entrypoint-initdb.d/seeds/country_utf8.csv'
DELIMITER ','
CSV HEADER;

CREATE TABLE IF NOT EXISTS country_language (
    country_code character(3) NOT NULL,
    "language" text NOT NULL,
    is_official boolean NOT NULL,
    percentage real NOT NULL
);

COPY country_language (country_code, language, is_official, percentage)
FROM '/docker-entrypoint-initdb.d/seeds/country_language_utf8.csv'
DELIMITER ','
CSV HEADER;

ALTER TABLE ONLY city
    ADD CONSTRAINT city_pkey PRIMARY KEY (id);

ALTER TABLE ONLY country
    ADD CONSTRAINT country_pkey PRIMARY KEY (code);

ALTER TABLE ONLY country_language
    ADD CONSTRAINT country_language_pkey PRIMARY KEY (country_code, "language");

ALTER TABLE ONLY country
    ADD CONSTRAINT country_capital_fkey FOREIGN KEY (capital) REFERENCES city(id);

ALTER TABLE ONLY country_language
    ADD CONSTRAINT country_language_country_code_fkey FOREIGN KEY (country_code) REFERENCES country(code);

COMMIT;