from dash import html, dcc, Output, Input, State, dash_table
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.express as px

from app import app
from services.classification_service import evaluate_classifier, save_model

evaluation = html.Div(id='classification-evaluation')


@app.callback(
    Output("classification-loading-output-1", "children"),
    Output("classification-evaluation", "children"),
    Input("classification-select-button", "n_clicks"),
    State("classification-demo-dropdown", "value")
)
def generate_model_button(n_clicks, filename):
    if n_clicks <= 0:
        raise PreventUpdate
    print("Confirm and continue: {}".format(filename))

    n_features, training_time, perf_metrics, cm, random_id, fig3, fig4 = evaluate_classifier(filename)

    fig = px.imshow(cm, title="Confusion matrix",
                    labels={'x': 'predicted (y_pred)', 'y': 'actual (y_test)'})

    print("returning update_evaluation")
    return filename, html.Div([
        html.H4("Classifier Evaluation"),
        html.P(
            "Use the information below to evaluate the classifier"),
        dbc.Row([
            dbc.Col([dcc.Graph(figure=fig)], xs=12, md=12, lg=6),
            dbc.Col([dcc.Graph(figure=fig3)], xs=12, md=12, lg=6),
            dbc.Col([dash_table.DataTable(
                data=perf_metrics.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in perf_metrics.columns],
                style_cell={"whiteSpace": "pre-line"},
                page_action="native",
                page_current=0,
                page_size=5,
            )], xs=12, md=12, lg=6),
            dbc.Col([dcc.Graph(figure=fig4)], xs=12, md=12, lg=6),
            html.P("Training time: {} seconds".format(training_time)),
            html.P("Number of features: {}".format(n_features)),
        ]),
        html.Br(),
        html.Br(),
        html.P("Save the model for further use"),
        dcc.Input(id="classification-model-name"),
        dbc.Button(id="classification-save-model", n_clicks=0, children='Save Model'),
        html.P(id="classification-temp-model-id", children=random_id)
    ])


@app.callback(
    Output("classification-model-saved", "children"),
    Input("classification-save-model", "n_clicks"),
    State("classification-model-name", "value"),
    State('classification-temp-model-id', 'children')
)
def classification_save_model(n_clicks, name, temp_model_id):
    if n_clicks <= 0:
        raise PreventUpdate

    save_model(name, temp_model_id)
    return html.P("Model {} saved".format(name))
