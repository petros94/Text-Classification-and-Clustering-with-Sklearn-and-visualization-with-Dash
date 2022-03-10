from dash import html, dcc, Output, Input, State, dash_table
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.express as px

from app import app
from routes.classification.constants import DIV_EVALUATION, LOADING_GENERATE_MODEL_OUTPUT, BUTTON_GENERATE_MODEL, \
    DROPDOWN_FILES, BUTTON_SAVE_MODEL, INPUT_MODEL_NAME, P_TEMP_MODEL_ID, DIV_MODEL_SAVED
from services.classification import train_evaluate, save_model

evaluation = html.Div(id=DIV_EVALUATION)


@app.callback(
    Output(LOADING_GENERATE_MODEL_OUTPUT, "children"),
    Output(DIV_EVALUATION, "children"),
    Input(BUTTON_GENERATE_MODEL, "n_clicks"),
    State(DROPDOWN_FILES, "value")
)
def generate_model_button(n_clicks, doc_id):
    if n_clicks <= 0:
        raise PreventUpdate
    print("Generate model pressed. Confirm and continue: {}".format(doc_id))

    n_features, training_time, perf_metrics, cm, random_id, fig3, fig4 = train_evaluate(doc_id)

    fig = px.imshow(cm, title="Confusion matrix",
                    labels={'x': 'predicted (y_pred)', 'y': 'actual (y_test)'})

    print("returning update_evaluation")
    return doc_id, html.Div([
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
        dcc.Input(id=INPUT_MODEL_NAME),
        dbc.Button(id=BUTTON_SAVE_MODEL, n_clicks=0, children='Save Model'),
        html.P(id=P_TEMP_MODEL_ID, children=random_id)
    ])


@app.callback(
    Output(DIV_MODEL_SAVED, "children"),
    Input(BUTTON_SAVE_MODEL, "n_clicks"),
    State(INPUT_MODEL_NAME, "value"),
    State(P_TEMP_MODEL_ID, 'children')
)
def classification_save_model(n_clicks, name, temp_model_id):
    if n_clicks <= 0:
        raise PreventUpdate

    save_model(name, temp_model_id)
    return html.P("Model {} saved".format(name))
