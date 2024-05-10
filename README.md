## Cities dwh build with dbt

You can find in this repo ELT process developed in dbt (data build tools) based on world_db sample database and countries API ('https://countriesnow.space/api/v0.1/countries/positions').

### Installation
This project uses postgres server and pgadmin to host dwh and handle all requests to it. Those two components are running on docker:
```
docker-compose up -d # will get you postgres running
```
dbt can be installed on venv with:
```
pip install dbt-postgres #specific to postgres agent
# alongside with other needed packages:
pip install sqlalchemy
pip install pandas
```

Note: Please reference png for the more detailed data structure/hierarchy inside ELT.

![Data model hierarchy (1)](https://github.com/shardev/dbt_pg_venv_docker/assets/26364512/5f1599f7-5d0e-4849-b6c9-7b4ceb9c803e)
