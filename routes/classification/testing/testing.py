import pandas as pd
from dash import html, dcc, Output, Input, State, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.exceptions import PreventUpdate

from app import app
from routes.classification.constants import *
from services.classification import predict_text_label
from services.storage import find_all_classifications_models, delete_classification_model

testing = html.Div([
    html.H4("Test classification"),
    html.P("Type a text to automatically label it. Give it a try!"),
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
    html.Div(id=DIV_CLASS_PROBS)
])


@app.callback(
    Output(DIV_CLASS_PROBS, 'children'),
    Input(BUTTON_MODEL_PREDICT, 'n_clicks'),
    State(DROPDOWN_MODELS, 'value'),
    State(TEXTAREA_MODEL_PREDICT, 'value')
)
def test_model(n_clicks, model, value):
    print("Entered test_model with args: {}, {}, {}".format(n_clicks, model, value))
    if n_clicks > 0 and model is not None:
        pred, testing_time = predict_text_label(model, value)
        fig = px.bar(pd.DataFrame(pred), x='label', y='pred')
        return dcc.Graph(figure=fig)


@app.callback(
    [
        Output(DROPDOWN_MODELS, "value"),
        Output(BUTTON_MODEL_PREDICT, "disabled")
    ],
    Input(DROPDOWN_MODELS, "options"),
)
def update_dropdown_value(options):
    print("update_dropdown_model entered with options: {}".format(options))
    if len(options) == 0:
        return None, True
    return options[len(options) - 1]['value'], False


@app.callback(
    Output(DROPDOWN_MODELS, 'options'),
    Input(DIV_MODEL_SAVED, 'children'),
    Input(DIV_DELETED_MODEL, 'children'),
    Input(BUTTON_HIDDEN, 'n_clicks'),
)
def update_dropdown_options(value, value_2, n_clicks):
    print("Entered update_dropdown_options")
    models = find_all_classifications_models()
    return list(map(lambda it: {"label": it['name'], "value": str(it['_id'])}, models))


@app.callback(
    Output(DIV_DELETED_MODEL, 'children'),
    Input(BUTTON_DELETE_MODEL, "n_clicks"),
    State(DROPDOWN_MODELS, "value")
)
def delete_model(n_clicks, model_id):
    if n_clicks > 0:
        print("called delete_model with arg: {}", model_id)
        if model_id is not None:
            return ["Deleted: " + delete_classification_model(model_id)]
