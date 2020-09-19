import re
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table


def find_poi(dataframe, column):
    # Find the point-of-interest in the column
    pattern = r"(\w*(?<=(gatan))\s\d+|\w*(?<=(vägen))\s\d+|\w*(?<=(vägen))|\w*(?<=(gatan)))"

    for row in dataframe[column]:
        try:
            (re.search(pattern, row.value)).group(0).isalpha()
            return (re.search(pattern, row.value)).group(0)
        except AttributeError:
            return "None"

    return True

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
