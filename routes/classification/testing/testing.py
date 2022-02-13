import pandas as pd
from dash import html, dcc, Output, Input, State, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.exceptions import PreventUpdate

from app import app
from config.cache import cache
from services.classification_service import predict_text_label
from services.cluster_service import predict_text_cluster

testing = html.Div([
    html.H4("Test classification"),
    html.P("Type a text to automatically label it. Give it a try!"),
    dbc.Row([
        dbc.Col([
            html.P("Choose model:"),
            dcc.Dropdown(id="classification-models-dropdown")
        ]),
        dbc.Col([
            dcc.Textarea(
                id='classification-textarea-state-example',
                style={'width': '100%', 'height': 200},
            ),
            dbc.Button(children='Submit', id='classification-test-model-button', n_clicks=0),
        ])
    ]),
    html.Div(id="class-probs")
])


@app.callback(
    Output('class-probs', 'children'),
    Input('classification-test-model-button', 'n_clicks'),
    State('classification-models-dropdown', 'value'),
    State('classification-textarea-state-example', 'value')
)
def test_model(n_clicks, model, value):
    print("Entered test_model with args: {}, {}, {}".format(n_clicks, model, value))
    if n_clicks > 0 and model is not None:
        pred, testing_time = predict_text_label(model, value)
        fig = px.bar(pd.DataFrame(pred), x='label', y='pred')
        return dcc.Graph(figure=fig)

@app.callback(
    Output("classification-models-dropdown", "value"),
    Input("classification-models-dropdown", "options"),
)
def update_dropdown_value(options):
    print("update_dropdown_model entered with options: {}".format(options))
    return options[len(options)-1]['label']

@app.callback(
    Output('classification-models-dropdown', 'options'),
    Input('classification-model-saved', 'children'),
    Input('classification-test-model-button', 'n_clicks'),
)
def update_dropdown_options(value, n_clicks):
    if n_clicks>0:
        raise PreventUpdate

    print("Entered update_dropdown_options")
    new_values = cache.get('classification-models')
    print("models cache is: ", new_values)
    return [{"label": it, "value": it} for it in new_values]