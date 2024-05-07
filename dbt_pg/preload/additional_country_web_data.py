import requests
import pandas as pd
from sqlalchemy import create_engine

# URL of the data
url = 'https://countriesnow.space/api/v0.1/countries/positions'
response = requests.get(url)

if response.status_code == 200:
    json_data = response.json()
    data = json_data['data']
    df = pd.DataFrame(data)

    db_user = 'admin'
    db_password = 'root'
    db_host = 'localhost'
    db_port = '5432'
    db_name = 'pg_db'
    
    engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    df.to_sql('country_api__country_locations', engine, index=False, if_exists='replace')
else:
    print("Failed to fetch data. Status code:", response.status_code)
