from src.postgresql import postgresql
import pandas as pd
from src.feature_engineering import weekday

# Setup database connection
psql = postgresql('polisen', '/home/tfidf/PycharmProjects/polisen_api/credentials/sql_credentials')
engine = psql.create_connection()

# Query the db: select records that are not appearing in fact_polisen
res = engine.execute("""
SELECT polisen_oltp.* FROM polisen_oltp
LEFT JOIN fact_polisen
ON polisen_oltp.id = fact_polisen.id
WHERE fact_polisen.id IS NULL
""")

# Get the dataframe
df = pd.DataFrame(data=res.fetchall(), columns=res.keys())

if len(df) > 0:
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
    nrOfRows = len(df)
    print("Transformed {0} rows".format(nrOfRows))
else:
    print("No new data to transform")
