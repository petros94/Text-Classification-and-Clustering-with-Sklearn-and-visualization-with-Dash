from dash import html, dcc
import dash_bootstrap_components as dbc

from routes.clustering.evaluation.cluster_evaluation import cluster_eval
from routes.clustering.stored.stored_component import stored
from routes.clustering.testing.cluster_testing import cluster_testing
from routes.clustering.tuning.cluster_tuning import cluster_tuning
from routes.clustering.upload.upload_component import upload

clustering = dbc.Container(
    [
        html.H1("Text Clustering App"),
        html.H5("This app is used to cluster text data using TFIDF and K-Means.", className="lead"),
        html.Hr(),
        html.Br(),
        html.Div([
            html.I(className="fas fa-hammer", style={'margin-right': 10, 'font-size': 'x-large', 'color': 'brown'}),
        ], style={'display': 'inline-block'}),
        html.Div([
            html.H2("Create a Model")
        ], style={'display': 'inline-block'}),
        html.Hr(),
        dbc.Row(
            [
                html.H4("Load data"),
                html.P("Upload csv/json files or choose one from the dropdown"),
                dbc.Col(upload, xs=6),
            ]
        ),
        dbc.Col(stored, xs=6),
        dbc.Button(id='select-button', n_clicks=0, children='Generate TFIDF & Tuning plots'),
        dcc.Loading(
            id="loading-1",
            type="default",
            children=html.Div(id="loading-output-1")
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        cluster_tuning,
        html.Br(),
        html.Br(),
        html.Br(),
        cluster_eval,
        html.Div(id="model-saved"),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Div([
            html.I(className="fas fa-play", style={'margin-right': 10, 'font-size': 'x-large', 'color': 'forestgreen'}),
        ], style={'display': 'inline-block'}),
        html.Div([
            html.H2("Use a Model")
        ], style={'display': 'inline-block'}),
        html.Hr(),
        cluster_testing,
        html.Div([
            dbc.Button(id="hidden-button", n_clicks=0, children="hidden", style={"display": "hidden"}),
        ], style={'display': 'none'}),
        dcc.Store(id='selected-dataset')
    ],
)
