from dash import html, dcc
import dash_bootstrap_components as dbc

from routes.classification.constants import *
from routes.classification.evaluation.evaluation import evaluation
from routes.classification.stored.stored_component import stored
from routes.classification.testing.testing import testing
from routes.classification.upload.upload_component import upload
from routes.classification.welcome.welcome import welcome

classification = dbc.Container([
    html.H1("Text Classification App"),
    html.H5("This app is used to classify text data using TFIDF and Naive Bayes.", className="lead"),
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
            html.P(
                "Upload csv/json files or choose one from the dropdown. The data will be 80/20 split to training and test set"),
            dbc.Col(upload, xs=6),
        ]
    ),
    dbc.Col(stored, xs=6),
    html.Div(id=DIV_STORED_DATA_PREVIEW),
    html.Br(),
    dbc.Button(id=BUTTON_GENERATE_MODEL, n_clicks=0, children='Generate TFIDF & Train Classifier', disabled=True),
    dcc.Loading(
        id=LOADING_GENERATE_MODEL,
        type="default",
        children=html.Div(id=LOADING_GENERATE_MODEL_OUTPUT)
    ),
    html.Br(),
    html.Br(),
    html.Br(),
    evaluation,
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
    testing,
    html.Div([
        dbc.Button(id=BUTTON_HIDDEN, n_clicks=0, children="hidden", style={"display": "hidden"}),
    ], style={'display': 'none'}),
])
