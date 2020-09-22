import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from src.postgresql import postgresql
import os


# Get data
#filepath_credentials = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials/sql_credentials')
#psql = postgresql('polisen', filepath_credentials)
psql = postgresql('polisen', 'credentials/sql_credentials')
engine = psql.create_connection()
res = engine.execute("""
SELECT fact_polisen.*, dim_crime.category 
FROM 
fact_polisen 
LEFT JOIN dim_crime
ON fact_polisen.type = dim_crime.type
ORDER BY 
datetime
""")
df = pd.DataFrame(data=res.fetchall(), columns=res.keys())
df['cc'] = 1
dimres = engine.execute('SELECT * FROM dim_crime')
dimcrime = pd.DataFrame(data=dimres.fetchall(), columns=dimres.keys())

# Dash app
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ['https://raw.githubusercontent.com/plotly/dash-app-stylesheets/master/dash-analytics-report.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

app.layout = html.Div(children=[
    html.H2(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    html.Label('Type Select'),
    dcc.Dropdown(
        id='type-dropdown',
        options=[{'label': value, 'value': value} for value in df.sort_values('type')['type'].unique().tolist()],
        value=['Rån väpnat'],
        multi=False
    ),
    html.Label('Category Select'),
    dcc.Dropdown(
        id='category-dropdown',
        options=[{'label': value, 'value': value} for value in dimcrime.sort_values('category')['category'].unique().tolist()],
        value='Bomb',
        multi=False
    ),

    dcc.Graph(
        id='event-timeline'
    )
])


# Implement callback
@app.callback(
    Output('event-timeline', 'figure'),
    [Input('category-dropdown', 'value')])
def update_figure(selected_category):
    print(selected_category)
    filtered_df = df[df.category == selected_category]
    fig = px.histogram(filtered_df, x="date", color="type", histfunc="count", nbins=df.date.nunique())

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
