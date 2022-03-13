from dash import dcc, html, Output, Input, State, dash_table
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from app import app
from routes.classification.constants import *
from services.storage import find_all_classification_docs, find_classification_doc_by_id, delete_classification_doc

stored = html.Div([
    dbc.Row([
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(id=DROPDOWN_FILES)
            ], xs=8),
            dbc.Col([
                dbc.Button(id=BUTTON_DELETE_DATASET, children='Delete', n_clicks=0, color="danger", outline=True)
            ], xs=4),
        ])
    ]),
    html.Div(id=DIV_DELETED_DATA),
    html.Br(),
])


def preview_df(doc_id):
    doc = find_classification_doc_by_id(doc_id)
    df = doc['content']
    return html.Div([
        html.H5(doc['filename']),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            style_cell={"whiteSpace": "pre-line"},
            page_action="native",
            page_current=0,
            page_size=5,
        ),

        html.Hr(),  # horizontal line

    ])


@app.callback(
    Output(DROPDOWN_FILES, "options"),
    Input(DIV_UPLOAD_DATA, "children"),
    Input(DIV_DELETED_DATA, "children"),
    Input(BUTTON_HIDDEN, 'n_clicks')
)
def load_dropdown(value, value2, n_clicks):
    docs = find_all_classification_docs()
    print("available docs: ", docs)
    return list(map(lambda it: {"label": it['filename'], "value": str(it['_id'])}, docs))


@app.callback(
    [Output(DROPDOWN_FILES, "value"),
     Output(BUTTON_GENERATE_MODEL, "disabled")],
    Input(DROPDOWN_FILES, "options"),
    State(UPLOAD_UPLOAD_DATA, 'filename')
)
def initialize_dropdown_value(options, filename):
    if len(options) == 0:
        return None, True
    return options[len(options) - 1]['value'], False


@app.callback(
    Output(DIV_STORED_DATA_PREVIEW, 'children'),
    Input(DROPDOWN_FILES, "value")
)
def update_preview(doc_id):
    print("called update_preview with arg: {}", doc_id)
    if doc_id is not None:
        return [preview_df(doc_id)]
    else:
        raise PreventUpdate


@app.callback(
    Output(DIV_DELETED_DATA, 'children'),
    Input(BUTTON_DELETE_DATASET, "n_clicks"),
    State(DROPDOWN_FILES, "value")
)
def delete_doc(n_clicks, doc_id):
    if n_clicks > 0:
        print("called delete_doc with arg: {}", doc_id)
        if doc_id is not None:
            return ["Deleted: " + delete_classification_doc(doc_id)]
