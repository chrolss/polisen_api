from sqlalchemy import create_engine, MetaData
import re
import pandas as pd


def transform_raw(raw_object):
    # The raw object has a nested shape and we want to explode that and transform to a new dict
    coordinates = re.findall(r'\d+\.\d+', raw_object['location']['gps'])

    transformed = {
        'id': raw_object['id'],
        'datetime': raw_object['datetime'],
        'name': raw_object['name'],
        'summary': raw_object['summary'],
        'url': raw_object['url'],
        'type': raw_object['type'],
        'location': raw_object['location']['name'],
        'longitude': coordinates[0],
        'latitude': coordinates[1]
    }

    return transformed


def list_of_json_to_df(json_list):
    data = []
    for event in json_list:
        data.append(transform_raw(event))

    df = pd.DataFrame(data)

    return df


def df_to_sql(engine, table, dataframe):
    _ = dataframe.to_sql(table, engine, if_exists='append', index=False)

    return True


def response_to_sql(json_list, engine, table):
    data = []
    for event in json_list:
        data.append(transform_raw(event))

    df = pd.DataFrame(data)
    _ = df.to_sql(table, engine, if_exists='append', index=False)

    return True
