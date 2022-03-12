from dash import dcc, html, Output, Input, State, dash_table
from dash.exceptions import PreventUpdate

from app import app
from routes.clustering.constants import *
from services.storage import find_all_cluster_docs, find_clustering_doc_by_id

stored = html.Div([
    dcc.Dropdown(id=DROPDOWN_FILES),
    html.Div(id=DIV_STORED_DATA_PREVIEW),
    html.Br(),
])

def preview_df(doc_id):
    doc = find_clustering_doc_by_id(doc_id)
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
    Input(BUTTON_HIDDEN, 'n_clicks')
)
def load_dropdown(value, n_clicks):
    docs = find_all_cluster_docs()
    print("available docs: ", docs)
    return list(map(lambda it: {"label": it['filename'], "value": str(it['_id'])}, docs))


@app.callback(
    Output(DROPDOWN_FILES, "value"),
    Input(DROPDOWN_FILES, "options"),
    State(UPLOAD_UPLOAD_DATA, 'filename')
)
def update_dropdown(options, filename):
    if len(options) == 0:
        raise PreventUpdate
    return options[len(options) - 1]['value']

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
