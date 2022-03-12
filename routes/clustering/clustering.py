from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc

from routes.clustering.constants import *
from routes.clustering.evaluation.cluster_evaluation import cluster_eval
from routes.clustering.stored.stored_component import stored
from routes.clustering.testing.cluster_testing import cluster_testing
from routes.clustering.tuning.cluster_tuning import cluster_tuning
from routes.clustering.upload.upload_component import upload
from routes.clustering.welcome.welcome import welcome

clustering = dbc.Container(
    [
        html.H1("Text Clustering App"),
        html.H5("This app is used to cluster text data using TFIDF and K-Means.", className="lead"),
        html.Hr(),
        welcome,
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
        dbc.Button(id=BUTTON_GENERATE_MODEL, n_clicks=0, children='Generate TFIDF & Tuning plots'),
        dcc.Loading(
            id=LOADING_GENERATE_MODEL,
            type="default",
            children=html.Div(id=LOADING_GENERATE_MODEL_OUTPUT)
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        cluster_tuning,
        html.Br(),
        html.Br(),
        html.Br(),
        cluster_eval,
        html.Div(id=DIV_MODEL_SAVED),
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
            dbc.Button(id=BUTTON_HIDDEN, n_clicks=0, children="hidden", style={"display": "hidden"}),
        ], style={'display': 'none'}),
    ],
)
