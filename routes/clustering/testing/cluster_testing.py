from dash import html, dcc, Output, Input, State, dash_table
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from app import app
from services.cluster_service import predict_text_cluster

cluster_testing = html.Div([
    html.H4("Test clustering"),
    html.P("Type a text and check which cluster fits best. Give it a try!"),
    dbc.Row([
        dbc.Col([
            html.P("Choose model:"),
            dcc.Dropdown(id="models-dropdown")
        ]),
        dbc.Col([
            dcc.Textarea(
                id='textarea-state-example',
                style={'width': '100%', 'height': 200},
            ),
            dbc.Button(children='Submit', id='test-model-button', n_clicks=0),
        ])
    ]),
    html.Div(id="textarea-state-example-output")
])


@app.callback(
    Output('textarea-state-example-output', 'children'),
    Input('test-model-button', 'n_clicks'),
    State('models-dropdown', 'value'),
    State('textarea-state-example', 'value')
)
def test_model(n_clicks, model, value):
    print("Entered test_model with args: {}, {}, {}".format(n_clicks, model, value))
    if n_clicks > 0 and model is not None:
        pred, top_terms = predict_text_cluster(model, value)
        return 'Text will be assigned to cluster: {}. Top terms for this cluster: {}'.format(str(pred), str(top_terms))
