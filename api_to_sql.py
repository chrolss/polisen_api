import requests
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table

key_file_path = 'sql_credentials'
keys = []
with open(key_file_path) as file:
    keys = file.read().splitlines()

sql_username = keys[0]
sql_password = keys[1]
ip = keys[2]

# Setup sqlengine and define table to write
engine_path = 'mssql+pyodbc://' + sql_username + ':' + sql_password + '@' + ip + '\\SQLEXPRESS/' + 'polisen' + '?driver=SQL+Server'
engine = create_engine(engine_path)
con = engine.connect()
#metadata = MetaData()
#metadata.reflect(engine)
#polisen_oltp_table = Table('polisen_oltp', metadata)

# Call the api and save the response to a dataframe
url = 'https://polisen.se/api/events'                  # Gets the 500 latest events
# url = 'https://polisen.se/api/events?DateTime=2019-01' # Gets the event for january 2019 (500 items max)
response = requests.get(url)
rjs = response.json()   # Save the response in json format for easy parsing, but this is a list containing dicts


def api_to_sql_date(date_string):
    f_url = 'https://polisen.se/api/events?DateTime=' + date_string   # Gets the event for january 2019 (500 items max)
    f_response = requests.get(f_url)
    f_rjs = f_response.json()
    idl = []
    datetimel = []
    namel = []
    summaryl = []
    urll = []
    typel = []
    location_namel = []
    longitudel = []
    latitudel = []

    for element in f_rjs:
        idl.append(element['id'])
        datetimel.append(element['datetime'])
        namel.append(element['name'])
        summaryl.append(element['summary'])
        urll.append(element['url'])
        typel.append(element['type'])
        location_namel.append(element['location']['name'])
        latlong_temp = element['location']['gps'].split(',')
        longitudel.append(latlong_temp[0])
        latitudel.append(latlong_temp[1])

    df = pd.DataFrame({'id': idl,
                      'datetime': datetimel,
                      'name': namel,
                      'summary': summaryl,
                      'url': urll,
                      'type': typel,
                      'location': location_namel,
                      'long': longitudel,
                      'lat': latitudel})

    _ = df.to_sql("polisen_oltp", engine, if_exists='append', index=False)

    return True


datelist = [str(i) if i > 9 else ('0' + str(i)) for i in range(1, 32)]
for date in datelist:
    api_to_sql_date(('2019-12-' + date))

