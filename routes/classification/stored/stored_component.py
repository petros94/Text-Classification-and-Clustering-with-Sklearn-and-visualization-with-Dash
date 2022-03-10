from dash import dcc, html, Output, Input, State, dash_table
from dash.exceptions import PreventUpdate

from app import app, cache
from routes.classification.constants import DROPDOWN_FILES, DIV_UPLOAD_DATA, BUTTON_HIDDEN, UPLOAD_UPLOAD_DATA
from services.storage import find_all_classification_docs

stored = html.Div([
    dcc.Dropdown(id=DROPDOWN_FILES),
    html.Br(),
])

@app.callback(
    Output(DROPDOWN_FILES, "options"),
    Input(DIV_UPLOAD_DATA, "children"),
    Input(BUTTON_HIDDEN, 'n_clicks')
)
def load_dropdown(value, n_clicks):
    docs = find_all_classification_docs()
    print("available docs: ", docs)
    return list(map(lambda it: {"label": it['filename'], "value": str(it['_id'])}, docs))

@app.callback(
    Output(DROPDOWN_FILES, "value"),
    Input(DROPDOWN_FILES, "options"),
    State(UPLOAD_UPLOAD_DATA, 'filename')
)
def initialize_dropdown_value(options, filename):
    if len(options) == 0:
        raise PreventUpdate
    return options[len(options)-1]['value']
