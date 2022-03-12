from dash import html, dcc, Output, Input, State, dash_table
import dash_bootstrap_components as dbc

from app import app
from routes.clustering.constants import *
from services.clustering import predict_text_cluster

cluster_testing = html.Div([
    html.H4("Test clustering"),
    html.P("Type a text and check which cluster fits best. Give it a try!"),
    dbc.Row([
        dbc.Col([
            html.P("Choose model:"),
            dcc.Dropdown(id=DROPDOWN_MODELS)
        ]),
        dbc.Col([
            dcc.Textarea(
                id=TEXTAREA_MODEL_PREDICT,
                style={'width': '100%', 'height': 200},
            ),
            dbc.Button(children='Submit', id=BUTTON_MODEL_PREDICT, n_clicks=0),
        ])
    ]),
    html.Div(id=DIV_CLUSTER_ASSIGN)
])


@app.callback(
    Output(DIV_CLUSTER_ASSIGN, 'children'),
    Input(BUTTON_MODEL_PREDICT, 'n_clicks'),
    State(DROPDOWN_MODELS, 'value'),
    State(TEXTAREA_MODEL_PREDICT, 'value')
)
def test_model(n_clicks, model, value):
    print("Entered test_model with args: {}, {}, {}".format(n_clicks, model, value))
    if n_clicks > 0 and model is not None:
        pred, top_terms, cluster_name = predict_text_cluster(model, value)
        return 'Text will be assigned to cluster {}: {}. Top terms for this cluster: {}'.format(str(pred), cluster_name, str(top_terms))
