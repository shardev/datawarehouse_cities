import requests
import pandas as pd
from sqlalchemy import create_engine
from constants import URL, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

response = requests.get(URL)

if response.status_code == 200:
    json_data = response.json()
    data = json_data['data']
    df = pd.DataFrame(data)

    engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    df.to_sql('country_api__country_locations', engine, index=False, if_exists='replace')
else:
    print("Failed to fetch data. Status code:", response.status_code)
