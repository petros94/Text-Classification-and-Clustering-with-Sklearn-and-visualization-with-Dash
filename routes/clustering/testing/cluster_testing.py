from dash import html, dcc, Output, Input, State, dash_table
import dash_bootstrap_components as dbc

from app import app
from routes.clustering.constants import *
from services.clustering import predict_text_cluster
from services.storage import delete_clustering_model

cluster_testing = html.Div([
    html.H4("Test clustering"),
    html.P("Type a text and check which cluster fits best. Give it a try!"),
    dbc.Row([
        dbc.Col([
            html.P("Choose model:"),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(id=DROPDOWN_MODELS)
                ], xs=8),
                dbc.Col([
                    dbc.Button(id=BUTTON_DELETE_MODEL, children='Delete', n_clicks=0, color="danger", outline=True)
                ], xs=4),
            ]),
            html.Div(id=DIV_DELETED_MODEL),
        ]),
        dbc.Col([
            dcc.Textarea(
                id=TEXTAREA_MODEL_PREDICT,
                style={'width': '100%', 'height': 200},
            ),
            dbc.Button(children='Submit', id=BUTTON_MODEL_PREDICT, n_clicks=0, disabled=True),
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
        return 'Text will be assigned to cluster {}: {}. Top terms for this cluster: {}'.format(str(pred), cluster_name,
                                                                                                str(top_terms))


@app.callback(
    Output(DIV_DELETED_MODEL, 'children'),
    Input(BUTTON_DELETE_MODEL, "n_clicks"),
    State(DROPDOWN_MODELS, "value")
)
def delete_model(n_clicks, model_id):
    if n_clicks > 0:
        print("called delete_model with arg: {}", model_id)
        if model_id is not None:
            return ["Deleted: " + delete_clustering_model(model_id)]
