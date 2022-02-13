import randomname
from dash import html, dcc, Output, Input, State, dash_table
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from app import app
from config.cache import cache
from services.cluster_service import evaluate_cluster, save_model

cluster_eval = html.Div([
    html.Div(id='evaluation')
])


@app.callback(
    Output('evaluation', 'children'),
    Input('select-n-clusters-button', 'n_clicks'),
    State('demo-dropdown', 'value'),
    State('n-clusters-slider', 'value')
)
def update_evaluation(n_clicks, filename, n_clusters):
    if filename is None or n_clicks<=0:
        raise PreventUpdate
    print("Confirm and continue {}".format(filename))
    clustered_data, top_terms, fig, img_sil, model_id = evaluate_cluster(n_clusters, filename)
    elements = []

    for term in top_terms:
        elements.append(html.Div([
            html.Div([
                dash_table.DataTable(
                    data=term.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in term.columns],
                    style_cell={"whiteSpace": "pre-line"},
                    page_action="native",
                    page_current=0,
                    page_size=5,
                )
            ])
        ]))
    print("returning update_evaluation")
    return html.Div([
        html.H4("Cluster Evaluation"),
        html.P("Use the information below to evaluate the cluster (Data points per cluster, silhouette score and samples per cluster)"),
        dbc.Row([
            dbc.Col([dcc.Graph(figure=fig)], xs=6),
            dbc.Col([html.Img(id='example', src=img_sil, style={'width': '100%'})], xs=6)
        ]),
        dbc.Col(elements),
        html.Br(),
        html.Br(),
        html.P("Save the model for further use"),
        dcc.Input(id="model-name"),
        dbc.Button(id="save-model", n_clicks=0, children='Save Model'),
        html.P(id="temp-model-id", children=model_id)
    ])


@app.callback(
    Output('model-saved', 'children'),
    Input('save-model', 'n_clicks'),
    State('model-name', 'value'),
    State('demo-dropdown', 'value'),
    State('n-clusters-slider', 'value'),
    State('temp-model-id', 'children')
)
def submit_save_model(n_clicks_save, model_name, filename, n_clusters, temp_model_id):
    print("Entered submit_save_model")
    if n_clicks_save>0:
        if model_name is None:
            model_name = randomname.get_name()
        save_model(model_name, n_clusters, filename, temp_model_id)
        return html.P("Model {} saved".format(model_name))
    else:
        raise PreventUpdate


@app.callback(
    Output("models-dropdown", "value"),
    Input("models-dropdown", "options"),
    State('model-name', 'filename')
)
def update_dropdown_value(options, filename):
    print("update_dropdown_model entered with options: {}".format(options))
    return options[len(options)-1]['label']

@app.callback(
    Output('models-dropdown', 'options'),
    Input('model-saved', 'children'),
    Input('test-model-button', 'n_clicks'),
)
def update_dropdown_options(value, n_clicks):
    if n_clicks>0:
        raise PreventUpdate

    print("Entered update_dropdown_options")
    new_values = cache.get('models')
    print("models cache is: ", new_values)
    return [{"label": it, "value": it} for it in new_values]