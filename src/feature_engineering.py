import re
import datetime


def weekday(fulldate):
    day_dict = {
        0: 'Måndag',
        1: 'Tisdag',
        2: 'Onsdag',
        3: 'Torsdag',
        4: 'Fredag',
        5: 'Lördag',
        6: 'Söndag'
    }
    return day_dict[datetime.datetime.weekday(fulldate)]


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


def get_street(textinput):
    # Do some regex magic
    pattern = r"(\w*(?<=(gatan))\s\d+|\w*(?<=(vägen))\s\d+|\w*(?<=(vägen))|\w*(?<=(gatan)))"
    try:
        (re.search(pattern, textinput)).group(0).isalpha()
        return (re.search(pattern, textinput)).group(0)
    except AttributeError:
        return "None"


def create_street_column(df):
    df['street'] = df.summary.apply(lambda x: get_street(x))
    return df
