from src.postgresql import postgresql
import pandas as pd
from src.feature_engineering import weekday

# Setup database connection
psql = postgresql('polisen', 'credentials/sql_credentials')
engine = psql.create_connection()

# Query the db
res = engine.execute("SELECT * FROM polisen_oltp")

# Get the dataframe
df = pd.DataFrame(data=res.fetchall(), columns=res.keys())

# Convert to datetime
df['datetime'] = pd.to_datetime(df['datetime'])

# Start with the feature engineering functions
df['weekday'] = df['datetime'].apply(lambda x: weekday(x))

# Create short date column
df['date'] = df['datetime'].apply(lambda x: x.date())

# Create clock
df['time'] = df['datetime'].apply(lambda x: x.hour)

# Insert into data model
_ = df.to_sql('fact_polisen', engine, if_exists='append', index=False)