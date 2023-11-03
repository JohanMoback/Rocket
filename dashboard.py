from flask import Flask, request, jsonify
import time
import requests
import concurrent.futures
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

app = Flask(__name__)
dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dashboard/')


@dash_app.callback(
    Output('dashboard-output', 'children'),
    [Input('start-button', 'n_clicks')]
)
def run_performance_test(n_clicks):
    data = {
        "url": "https://example.com",
        "numRequests": 100,
        "rampUpDuration": 10,
        "timeout": 10
    }

    response = rocket(data)
    return f"Performance Test Completed: {response}"


@dash_app.callback(
    Output('response-time-chart', 'figure'),
    [Input('view-response-time-button', 'n_clicks')]
)
def view_response_time_chart(n_clicks):
    # Fetch response time data from your Flask app
    # Replace this with your own code to retrieve the response time data
    response_time_data = [150, 140, 160, 155, 170]

    figure = px.line(x=list(range(1, len(response_time_data) + 1)), y=response_time_data,
                     title='Response Time Over Time')
    return figure


@dash_app.callback(
    Output('throughput-chart', 'figure'),
    [Input('view-throughput-button', 'n_clicks')]
)
def view_throughput_chart(n_clicks):
    # Fetch throughput data from your Flask app
    # Replace this with your own code to retrieve the throughput data
    throughput_data = [20, 22, 18, 21, 19]

    figure = px.line(x=list(range(1, len(throughput_data) + 1)), y=throughput_data, title='Throughput Over Time')
    return figure


@dash_app.callback(
    Output('start-button', 'disabled'),
    Output('view-response-time-button', 'disabled'),
    Output('view-throughput-button', 'disabled'),
    [Input('dashboard-output', 'children')]
)
def update_button_states(output):
    if "Performance Test Completed" in output:
        return True, False, False
    else:
        return False, True, True


if __name__ == '__main__':
    dash_app.layout = html.Div([
        html.H1("Performance Test Dashboard"),
        dcc.Graph(id='response-time-chart'),
        dcc.Graph(id='throughput-chart'),
        html.Button("Start Test", id='start-button', n_clicks=0),
        html.Button("View Response Time Chart", id='view-response-time-button', n_clicks=0),
        html.Button("View Throughput Chart", id='view-throughput-button', n_clicks=0),
        html.Div(id='dashboard-output')
    ])

    app.run(debug=True)
