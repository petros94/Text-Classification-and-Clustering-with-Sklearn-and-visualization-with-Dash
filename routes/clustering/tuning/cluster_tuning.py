from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc

from app import app
from services.cluster_service import evaluate_cluster, generate_optimal_cluster_figures

cluster_tuning = html.Div(id="cluster_tuning")

@app.callback(
    Output("loading-output-1", "children"),
    Output('cluster_tuning', 'children'),
    Input('select-button', 'n_clicks'),
    State('demo-dropdown', 'value')
)
def update_output(n_clicks, value):
    print("Selected ", value)
    fig1, fig2 = generate_optimal_cluster_figures(value)
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
                    dcc.Slider(min=2, max=20, dots=True,
                               value=2,
                               tooltip={"placement": "bottom", "always_visible": True},
                               id='n-clusters-slider'
                               ),
                    html.Div(id='n-clusters-slider-output-container')
                ], xs=6),
            ])])
        ,
        dbc.Button(id='select-n-clusters-button', n_clicks=0, children='Confirm and evaluate'),
    ])


@app.callback(
    Output('n-clusters-slider-output-container', 'children'),
    Input('n-clusters-slider', 'value'))
def update_output(value):
    return 'You have selected "{}"'.format(value)
