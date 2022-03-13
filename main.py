"""
This app creates a simple sidebar layout using inline style arguments and the
dbc.Nav component.

dcc.Location is used to track the current location, and a callback uses the
current location to render the appropriate page content. The active prop of
each NavLink is set automatically according to the current pathname. To use
this feature you must install dash-bootstrap-components >= 0.11.0.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""
import os

import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input
from app import app
from routes.classification.classification import classification
from routes.clustering.clustering import clustering

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

sidebar = html.Div(
    [
        html.H2("TextML", className="display-4"),
        dbc.Row([html.H6("Easy clustering + classification for text", className="display-12")]),
        dbc.Nav(
            [
                dbc.NavLink("Text Clustering Tool", href="/", active="exact"),
                dbc.NavLink("Text Classification Tool", href="/classification", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
content = html.Div(id="page-content", style=CONTENT_STYLE)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    print(pathname)
    if pathname == "/":
        return clustering
    elif pathname == "/classification":
        return classification

    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

server = app.server
if __name__ == "__main__" and os.environ.get("PROFILE") != "prod":
    app.run_server(port=8080, debug=True, host="0.0.0.0")
