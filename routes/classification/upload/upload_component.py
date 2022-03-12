import base64
import datetime
import io
import pickle

import pandas as pd
from dash import dcc, html, Output, Input, State, dash_table
from dash.exceptions import PreventUpdate

from app import app, cache
from routes.classification.constants import *
from services.storage import insert_classification_doc, find_classification_doc_by_id

upload = html.Div([
    dcc.Upload(
        id=UPLOAD_UPLOAD_DATA,
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id=DIV_UPLOAD_DATA, style={"display": "hidden"}),
])


def parse_contents(contents, filename, date):
    df = None
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))[['input', 'label']] \
                .dropna() \
                .reset_index()
        elif 'json' in filename:
            df = pd.read_json(io.StringIO(decoded.decode('utf-8')), lines=True)[['input', 'label']] \
                .dropna() \
                .reset_index()
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    if df is not None:
        insert_classification_doc(filename, df)
        print("Stored file in storage", filename)

    return html.P(children=filename)


@app.callback(
    Output(DIV_UPLOAD_DATA, 'children'), [
    Input(UPLOAD_UPLOAD_DATA, 'contents'),
    State(UPLOAD_UPLOAD_DATA, 'filename'),
    State(UPLOAD_UPLOAD_DATA, 'last_modified')
])
def update_output(list_of_contents, list_of_names, list_of_dates):
    print("callback upload component")
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children
    else:
        raise PreventUpdate