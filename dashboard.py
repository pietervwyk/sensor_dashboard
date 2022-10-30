from dash.dependencies import Input, Output, State
from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dashboard_styles import center, title

server = Flask(__name__)
app = Dash(__name__, server=server, suppress_callback_exceptions=False)
app.server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.server.config["SQLALCHEMY_DATABASE_URI"] = "INSERT_DB_STRING"
db = SQLAlchemy(app.server)

def serve_layout():
    df_unsorted = pd.read_sql_table('sensor_table', con=db.engine)
    df = df_unsorted.sort_values(by = 'timestamp')
    return html.Div(children=[
        html.H1(children="Pieter's Skripsie - Remote Data Logger", style=title()),
        html.H2(children="Currently stationed in Helshoogte, Sample Interval = 5min", style=title()),
        dcc.Interval(
            id='interval-component',
            interval=5*60*1000, # in milliseconds
            n_intervals=0
        ),

        dcc.Graph(
            id='wind_graph',
            figure={
                'data': [go.Scatter(x=df['timestamp'], y=df['wind'], connectgaps=True)],
                'layout': {'title': 'Wind Speed [km/h]'}
        }),
        
        dcc.Graph(
            id='uv_graph',
            figure={
                'data': [go.Scatter(x=df['timestamp'], y=df['uv'], connectgaps=True)],
                'layout': {'title': 'UV Index'}
        }),

        dcc.Graph(
            id='temperature_graph',
            figure={
                'data': [go.Scatter(x=df['timestamp'], y=df['temperature'], connectgaps=True)],
                'layout': {'title': 'Temperature [°C]'}
        }),

        dcc.Graph(
            id='humidity_graph',
            figure={
                'data': [go.Scatter(x=df['timestamp'], y=df['humidity'], connectgaps=True)],
                'layout': {'title': 'Humidity [g/kg]'}
        }),
])

@app.callback(Output('wind_graph', 'figure'),
              Output('uv_graph', 'figure'),
              Output('temperature_graph', 'figure'),
              Output('humidity_graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def refresh_graphs(n):
    df_unsorted = pd.read_sql_table('sensor_table', con=db.engine)
    df = df_unsorted.sort_values(by = 'timestamp')
    wind_fig={
        'data': [go.Scatter(x=df['timestamp'], y=df['wind'])],
        'layout': {'title': 'Wind Speed - ' + str(df.wind.iloc[-1]) + 'km/h'}
    }
    uv_fig={
        'data': [go.Scatter(x=df['timestamp'], y=df['uv'])],
        'layout': {'title': 'UV Index - ' + str(df.uv.iloc[-1])}
    }
    temperature_fig={
        'data': [go.Scatter(x=df['timestamp'], y=df['temperature'])],
        'layout': {'title': 'Temperature - ' + str(df.temperature.iloc[-1]) + '°C'}
    }
    humidity_fig={
        'data': [go.Scatter(x=df['timestamp'], y=df['humidity'])],
        'layout': {'title': 'Humidity - ' + str(df.humidity.iloc[-1]) + '%'}
    }
    return wind_fig, uv_fig, temperature_fig, humidity_fig

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=False)
