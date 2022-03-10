import base64
import datetime
import io

import pandas as pd
from dash import dcc, html, Output, Input, State, dash_table
import dash_bootstrap_components as dbc

from app import app, cache
from services.clustering import TextClustering, generate_optimal_cluster_figures
from util import TextPreprocessor

stored = html.Div([
    dcc.Dropdown(id='demo-dropdown'),
    html.Br(),
])

@app.callback(
    Output("demo-dropdown", "options"),
    Input("output-data-upload", "children"),
    Input('hidden-button', 'n_clicks')
)
def update_dropdown(value, n_clicks):
    new_values = cache.get('files')
    print("data cache is: ",new_values)
    return [{"label": it, "value": it} for it in new_values]


@app.callback(
    Output("demo-dropdown", "value"),
    Input("demo-dropdown", "options"),
    State('upload-data', 'filename')
)
def update_dropdown(options, filename):
    return options[len(options)-1]['label']
