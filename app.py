import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from src.postgresql import postgresql

# Get data
psql = postgresql('polisen', 'credentials/sql_credentials')
engine = psql.create_connection()
res = engine.execute('SELECT * FROM fact_polisen')
df = pd.DataFrame(data=res.fetchall(), columns=res.keys())
df['cc'] = 1

# Dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

fig = px.bar(df[df['type'] == 'Rån väpnat'], x="date", y="cc", color="type", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
