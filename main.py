from src.polisen_api import PolisenAPI
from src.json_to_sql import response_to_sql
from src.postgresql import postgresql
import pandas as pd
import datetime
import time

# Initialize the Polisen API
api = PolisenAPI()

# Setup database connection
psql = postgresql('polisen', 'credentials/sql_credentials')
engine = psql.create_connection()

# Work through the dates and pull the events based on the latest in the SQL server
sql_response = engine.execute('SELECT MAX(datetime) FROM polisen_oltp').fetchall()
working_date = datetime.datetime.strptime(sql_response[0][0], '%Y-%m-%d %H:%M:%S %z') + datetime.timedelta(days=1)
#working_date = datetime.datetime.strptime('2020-04-01', '%Y-%m-%d')

work = False # To see if we did work
while working_date.date() < datetime.datetime.now().date():
    work = True
    # Fetch the events for a specific date, insert into SQL database, and then wait 2 secs to not overload the API
    temp_data = api.get_date_events(working_date.strftime('%Y-%m-%d'))
    _ = response_to_sql(json_list=temp_data, engine=engine, table='polisen_oltp')
    print("Inserted {0} rows from {1}".format(len(temp_data), working_date.strftime('%Y-%m-%d')))
    time.sleep(2)
    working_date = working_date + datetime.timedelta(days=1)

if work:
    print("Done with the work")
else:
    print("No new data to download")
