from dash import dcc, html, Output, Input, State, dash_table

from app import app, cache


stored = html.Div([
    dcc.Dropdown(id='classification-demo-dropdown'),
    html.Br(),
])

@app.callback(
    Output("classification-demo-dropdown", "options"),
    Input("classification-output-data-upload", "children"),
    Input('hidden-button-2', 'n_clicks')
)
def update_dropdown(value, n_clicks):
    new_values = cache.get('classification-files')
    print("classification-cache is: ",new_values)
    return [{"label": it, "value": it} for it in new_values]


@app.callback(
    Output("classification-demo-dropdown", "value"),
    Input("classification-demo-dropdown", "options"),
    State('classification-upload-data', 'filename')
)
def update_dropdown(options, filename):
    return options[len(options)-1]['label']
