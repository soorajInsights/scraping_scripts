import requests
from fake_useragent import UserAgent
import psycopg2

api_url = "https://www.carwale.com/api/v4/autocomplete/?source=1%2C2%2C3%2C5%2C11%2C15%2C13%2C14%2C10%2C16%2C17%2C4%2C8%2C9%2C6%2C19%2C20%2C21%2C22%2C23%2C24%2C25%2C26%2C27%2C28%2C29&value=mahindra&size=20&applicationId=1&showNoResult=true&cityId=-1"

ua = UserAgent()

header = {"User-Agent":ua.random}

response = requests.get(api_url,headers=header,timeout=10)
response.raise_for_status()

data = response.json()

filter_data = []
for item in data:
    items = {
        "modelName": item["payload"].get("modelName"),
        "makeName" : item["payload"].get("makeName")
    }
    filter_data.append(items)

for modelname in filter_data:
    print(modelname)
print("\n Data fetched successfully")


#Database part
postgres_configuration = {
    "dbname": "car_db",
    "user" : "car_user",
    "password": "car_pass",
    "host":"localhost",
    "port":"5432"
}

conn = psycopg2.connect(**postgres_configuration
)

cur =conn.cursor()

cur.execute("""CREATE TABLE car_models(
        id SERIAL PRIMARY KEY,
        make_name TEXT,
        model_name TEXT
    );
""")

for item in filter_data:
    cur.execute("""
            INSERT INTO car_models
                (make_name,model_name)
                VALUES (%s,%s);
""",(item["makeName"],item["modelName"]))

conn.commit()

cur.close()
conn.close()

print("\nData Insert into postgreSQL")