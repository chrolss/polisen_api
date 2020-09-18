import re
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

# Get table content
df = pd.read_sql("SELECT * FROM polisen_oltp;", con)

# Do some regex magic
pattern = r"(\w*(?<=(gatan))\s\d+|\w*(?<=(vägen))\s\d+|\w*(?<=(vägen))|\w*(?<=(gatan)))"

def get_street(r, textinput):
    try:
        (re.search(r, textinput)).group(0).isalpha()
        return (re.search(r, textinput)).group(0)
    except AttributeError:
        return "None"


df['street'] = df.summary.apply(lambda x: get_street(pattern, x))
