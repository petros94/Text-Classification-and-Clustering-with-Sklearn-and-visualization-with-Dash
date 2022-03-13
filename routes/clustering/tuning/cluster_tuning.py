from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from app import app
from routes.clustering.constants import *
from services.clustering import generate_optimal_cluster_figures

cluster_tuning = html.Div(id=DIV_TUNING)

@app.callback(
    Output(LOADING_GENERATE_MODEL_OUTPUT, "children"),
    Output(DIV_TUNING, 'children'),
    Input(BUTTON_GENERATE_MODEL, 'n_clicks'),
    State(DROPDOWN_FILES, 'value'),
    State(TEXTAREA_COMMON_WORDS, 'value')
)
def update_output(n_clicks, value, words):
    if n_clicks <= 0:
        raise PreventUpdate

    print("generate model ", value, words)
    fig1, fig2 = generate_optimal_cluster_figures(value, words.replace(" ", "").split(",") if words is not None else None)
    return value, html.Div([
        dbc.Row([
            html.H4("Choose number of clusters"),
            html.P("Consult the diagrams below to select the best number of clusters"),
            dbc.Col([
                dbc.Row(
                    [
                        dcc.Graph(figure=fig1),
                    ]
                ),
            ], xs=6),
            dbc.Col([
                dbc.Row(
                    [
                        dcc.Graph(figure=fig2),
                    ]
                ),
            ], xs=6),
            html.Div([
                dbc.Col([
                    dcc.Slider(min=2, max=20, dots=True, step=1,
                               value=2,
                               tooltip={"placement": "bottom", "always_visible": True},
                               id=SLIDER_N_CLUSTERS
                               ),
                    html.Div(id=DIV_N_CLUSTERS)
                ], xs=6),
            ])])
        ,
        dbc.Button(id=BUTTON_SELECT_CLUSTERS, n_clicks=0, children='Confirm and evaluate'),
    ])


@app.callback(
    Output(DIV_N_CLUSTERS, 'children'),
    Input(SLIDER_N_CLUSTERS, 'value'))
def update_output(value):
    return 'You have selected "{}"'.format(value)
