from dash import html
import dash_bootstrap_components as dbc

welcome = html.Div([
    html.Div([
        html.I(className="fas fa-info", style={'margin-right': 10, 'font-size': 'x-large', 'color': 'blue'}),
    ], style={'display': 'inline-block'}),
    html.Div([
        html.H2("Instructions")
    ], style={'display': 'inline-block'}),
    html.Hr(),
    dbc.Row([
        html.P(
            "This tool is used on text data to predict the text label. You can upload the data in csv or json format. "
            "The data need to have a column named \"input\" which contains the raw text sentence, and a column \"label\" with "
            "the corresponding label. Each row of the dataset "
            "represents a different text document. The tool performs a TFIDF transform of the dataset to obtain the feature "
            "vector and trains a naive bayes classifier using the provided labels. Then you can provide new samples and use the "
            "model to predict their label. Keep in mind that bigger datasets may take longer to process.")
    ])
])
