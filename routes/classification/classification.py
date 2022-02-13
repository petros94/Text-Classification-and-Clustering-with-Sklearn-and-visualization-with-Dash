from dash import html, dcc
import dash_bootstrap_components as dbc

from routes.classification.evaluation.evaluation import evaluation
from routes.classification.stored.stored_component import stored
from routes.classification.testing.testing import testing
from routes.classification.upload.upload_component import upload

classification = dbc.Container([
    html.H1("Text Classification App"),
    html.H5("This app is used to classify text data using TFIDF and Naive Bayes.", className="lead"),
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
            html.P(
                "Upload csv/json files or choose one from the dropdown. The data will be 80/20 split to training and test set"),
            dbc.Col(upload, xs=6),
        ]
    ),
    dbc.Col(stored, xs=6),
    dbc.Button(id='classification-select-button', n_clicks=0, children='Generate TFIDF & Train Classifier'),
    dcc.Loading(
        id="classification-loading-1",
        type="default",
        children=html.Div(id="classification-loading-output-1")
    ),
    html.Br(),
    html.Br(),
    html.Br(),
    evaluation,
    html.Div(id="classification-model-saved"),
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
        dbc.Button(id="hidden-button-2", n_clicks=0, children="hidden", style={"display": "hidden"}),
    ], style={'display': 'none'}),
])
