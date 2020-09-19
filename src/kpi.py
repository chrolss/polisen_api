import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.postgresql import postgresql

psql = postgresql('polisen', 'credentials/sql_credentials')
engine = psql.create_connection()

result = engine.execute('SELECT * FROM polisen_oltp')
df = pd.DataFrame(data=result.fetchall(), columns=result.keys())

_ = plt.plot(df[['type'] == 'Misshandel']['datetime'])
