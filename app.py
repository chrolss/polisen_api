# -*- coding: latin-1 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from src.postgresql import postgresql
import dash_daq as daq

# Get data
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
df['week'] = df['datetime'].apply(lambda x: x.isocalendar()[1])  # Gets the week number
dimres = engine.execute('SELECT * FROM dim_crime')
dimcrime = pd.DataFrame(data=dimres.fetchall(), columns=dimres.keys())

# Dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
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
        options=[{'label': value, 'value': value} for value in
                 dimcrime.sort_values('category')['category'].unique().tolist()],
        value='Bomb',
        multi=False
    ),

    dcc.Graph(
        id='event-timeline'
    ),
    daq.Indicator(
        id='kpi-indicator',
        label="Red",
        color="red",
        value=True
    )
])


# Implement callback
@app.callback(
    dash.dependencies.Output('type-dropdown', 'options'),
    [dash.dependencies.Input('category-dropdown', 'value')]
)
def update_date_dropdown(name):
    return [{'label': i, 'value': i} for i in dimcrime[dimcrime['category'] == name]
            .sort_values('type')['type'].tolist()]


@app.callback(
    Output('event-timeline', 'figure'),
    [Input('category-dropdown', 'value'),
     Input('type-dropdown', 'value')])
def update_figure_filter_category(selected_category, selected_type):
    ctx = dash.callback_context
    print(ctx.triggered[0]['prop_id'])
    if ctx.triggered[0]['prop_id'] == 'category-dropdown.value':
        filtered_df = df[df.category == selected_category]
    elif ctx.triggered[0]['prop_id'] == 'type-dropdown.value':
        filtered_df = df[df.type == selected_type]
    else:
        filtered_df = df[df.category == 'Bomb']
    # fig = px.histogram(filtered_df, x="date", color="type", histfunc="count", nbins=df.date.nunique())
    fig = px.histogram(filtered_df, x="week", color="type", histfunc="count", nbins=df.week.nunique())
    fig.update_layout(transition_duration=500)

    return fig


@app.callback(
    Output('kpi-indicator', 'label'),
    [Input('category-dropdown', 'value')]
)
def update_kpi(selected_category):
    temp_df = df[df['category'] == selected_category]
    temp_df.index = temp_df.datetime
    temp_df = temp_df.resample('1D').sum().fillna(0)
    temp_df.rolling('7D')['cc'].mean().plot()
    current_week = temp_df.iloc[-8:-1]['cc'].sum() / 7  # last 7 days
    previous_week = temp_df.iloc[-14:-7]['cc'].sum() / 7  # previous 7 day period
    if current_week > previous_week:
        diff = (- 1 + (float(current_week) / float(previous_week))) * 100.0
    else:
        diff = ((float(current_week) / float(previous_week)) - 1) * 100.0
    print(diff)
    return "{:.2f}".format(diff)


if __name__ == '__main__':
    app.run_server(debug=True)
