import randomname
from dash import html, dcc, Output, Input, State, dash_table
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from app import app
from models.text_cluster import load_model
from routes.clustering.constants import *
from services.clustering import evaluate_cluster, save_model
from services.storage import find_all_cluster_models

cluster_eval = html.Div([
    html.Div(id=DIV_EVALUATION)
])


@app.callback(
    Output(LOADING_EVAL_MODEL_OUTPUT, "children"),
    Output(DIV_EVALUATION, 'children'),
    Input(BUTTON_SELECT_CLUSTERS, 'n_clicks'),
    State(DROPDOWN_FILES, 'value'),
    State(SLIDER_N_CLUSTERS, 'value'),
    State(TEXTAREA_COMMON_WORDS, 'value')
)
def update_evaluation(n_clicks, filename, n_clusters, words):
    if filename is None or n_clicks <= 0:
        raise PreventUpdate
    print("Confirm and continue {}, {}, {}".format(filename, n_clusters, words))
    clustered_data, top_terms, fig, img_sil, model_id = evaluate_cluster(n_clusters, filename, words.replace(" ", "").split(",") if words is not None else None)
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
    return n_clusters, html.Div([
        html.H4("Cluster Evaluation"),
        html.P(
            "Use the information below to evaluate the cluster (Data points per cluster, silhouette score and samples per cluster)"),
        dbc.Row([
            dbc.Col([dcc.Graph(figure=fig)], xs=6),
            dbc.Col([html.Img(id='example', src=img_sil, style={'width': '100%'})], xs=6)
        ]),
        dbc.Col(elements),
        html.Br(),
        html.Br(),
        html.H4("Label the clusters"),
        html.P("Give the clusters a human-friendly name based on their content"),
        dbc.Row([
            dcc.Store(id=STORE_CLUSTER_NAMES, data={'names': ['cluster-' + str(i) for i in range(n_clusters)]}),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(id=DROPDOWN_CLUSTER_NAMES,
                                 options=[{'label': 'Cluster ' + str(i), 'value': i} for i in range(n_clusters)])
                ], xs=2),
                dbc.Col([
                    dcc.Input(id=INPUT_CLUSTER_NAMES)
                ], xs=4),
            ])
        ]),
        html.Br(),
        html.H4("Save and Download"),
        html.P("Save the model for further use and download the labeled dataset"),
        dcc.Input(id=INPUT_MODEL_NAME),
        dbc.Button(id=BUTTON_SAVE_MODEL, n_clicks=0, children='Save Model'),
        html.P(id=P_TEMP_MODEL_ID, children=model_id),
        dbc.Button(id=BUTTON_DOWNLOAD, n_clicks=0, children='Download Data'),
        dcc.Download(id=DOWNLOAD_DATA)
    ])


@app.callback(
    Output(INPUT_CLUSTER_NAMES, 'value'),
    Input(DROPDOWN_CLUSTER_NAMES, 'value'),
    State(STORE_CLUSTER_NAMES, 'data')
)
def on_dropdown_change(dr_val, data):
    if dr_val is not None:
        return data['names'][dr_val]


@app.callback(
    Output(STORE_CLUSTER_NAMES, 'data'),
    Input(INPUT_CLUSTER_NAMES, 'value'),
    State(DROPDOWN_CLUSTER_NAMES, 'value'),
    State(STORE_CLUSTER_NAMES, 'data')
)
def on_input_change(input_val, dr_val, data):
    if dr_val is None:
        dr_val = 0
    if input_val in [None, '']:
        input_val = 'cluster-' + str(dr_val)
    data['names'][dr_val] = input_val
    return data


@app.callback(
    Output(DIV_MODEL_SAVED, 'children'),
    Input(BUTTON_SAVE_MODEL, 'n_clicks'),
    State(INPUT_MODEL_NAME, 'value'),
    State(DROPDOWN_FILES, 'value'),
    State(SLIDER_N_CLUSTERS, 'value'),
    State(P_TEMP_MODEL_ID, 'children'),
    State(STORE_CLUSTER_NAMES, 'data')
)
def submit_save_model(n_clicks_save, model_name, filename, n_clusters, temp_model_id, cluster_names):
    print("Entered submit_save_model")
    if n_clicks_save > 0:
        if model_name is None:
            model_name = randomname.get_name()
        save_model(model_name, n_clusters, filename, temp_model_id, cluster_names['names'])
        return html.P("Model {} saved".format(model_name))
    else:
        raise PreventUpdate


@app.callback(
    [
        Output(DROPDOWN_MODELS, "value"),
        Output(BUTTON_MODEL_PREDICT, "disabled")
    ],
    Input(DROPDOWN_MODELS, "options")
)
def update_dropdown_value(options):
    print("update_dropdown_model entered with options: {}".format(options))
    if len(options) == 0:
        return None, True
    return options[len(options) - 1]['value'], False


@app.callback(
    Output(DROPDOWN_MODELS, 'options'),
    Input(DIV_UPLOAD_DATA, 'children'),
    Input(DIV_DELETED_MODEL, 'children'),
    Input(BUTTON_HIDDEN, 'n_clicks'),
)
def update_dropdown_options(value, value_2, n_clicks):
    print("Entered model update_dropdown_options")
    models = find_all_cluster_models()
    return list(map(lambda it: {"label": it['name'], "value": str(it['_id'])}, models))


@app.callback(
    Output(DOWNLOAD_DATA, 'data'),
    Input(BUTTON_DOWNLOAD, 'n_clicks'),
    State(P_TEMP_MODEL_ID, 'children'),
    State(STORE_CLUSTER_NAMES, 'data'),
    prevent_initial_call=True
)
def download_data(n_clicks, temp_model_id, cluster_names):
    print("Entered download_data")
    tcl = load_model(temp_model_id, temp=True)
    tcl.cluster_names = cluster_names['names']
    df = tcl.clustered_data
    df['label'] = df['pred'].apply(lambda it: cluster_names['names'][int(it)])
    return dcc.send_data_frame(df.to_csv, 'clustered_data.csv')
