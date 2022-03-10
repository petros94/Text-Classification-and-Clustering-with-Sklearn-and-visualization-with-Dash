import pandas as pd
from dash import html, dcc, Output, Input, State, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.exceptions import PreventUpdate

from app import app
from routes.classification.constants import DROPDOWN_MODELS, TEXTAREA_MODEL_PREDICT, BUTTON_MODEL_PREDICT, \
    DIV_CLASS_PROBS, DIV_MODEL_SAVED
from services.classification import predict_text_label
from services.storage import find_all_classifications_models

testing = html.Div([
    html.H4("Test classification"),
    html.P("Type a text to automatically label it. Give it a try!"),
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
    Output(DROPDOWN_MODELS, "value"),
    Input(DROPDOWN_MODELS, "options"),
)
def update_dropdown_value(options):
    print("update_dropdown_model entered with options: {}".format(options))
    if len(options) == 0:
        raise PreventUpdate
    return options[len(options)-1]['value']

@app.callback(
    Output(DROPDOWN_MODELS, 'options'),
    Input(DIV_MODEL_SAVED, 'children'),
    Input(BUTTON_MODEL_PREDICT, 'n_clicks'),
)
def update_dropdown_options(value, n_clicks):
    if n_clicks > 0:
        raise PreventUpdate

    print("Entered update_dropdown_options")
    models = find_all_classifications_models()
    return list(map(lambda it: {"label": it['name'], "value": str(it['_id'])}, models))