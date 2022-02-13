import base64
import datetime
import io

import pandas as pd
from dash import dcc, html, Output, Input, State, dash_table
from dash.exceptions import PreventUpdate

from app import app, cache

upload = html.Div([
    dcc.Upload(
        id='classification-upload-data',
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
    html.Div(id='classification-output-data-upload'),
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
        files = cache.get('classification-files')
        files.append(filename)

        cache.set(filename, df)
        cache.set('classification-files', files)
        print("Stored in classification-cache", filename)

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data = df.to_dict('records'),
            columns = [{'name': i, 'id': i} for i in df.columns],
            style_cell={"whiteSpace": "pre-line"},
            page_action="native",
            page_current=0,
            page_size=5,
        ),

        html.Hr(),  # horizontal line

    ])


@app.callback(
    Output('classification-output-data-upload', 'children'), [
    Input('classification-upload-data', 'contents'),
    State('classification-upload-data', 'filename'),
    State('classification-upload-data', 'last_modified')
])
def update_output(list_of_contents, list_of_names, list_of_dates):
    print("callback upload component")
    print(cache.get('classification-files'))
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children
    else:
        raise PreventUpdate
