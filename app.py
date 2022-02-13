import dash
import dash_bootstrap_components as dbc
import pandas as pd

from config.cache import cache, config

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
cache.init_app(app.server, config=config)
cache.set('models', [])
cache.set('classification-models', [])

# Load initial data
df = pd.read_csv('demo/datasets/samples_200_per_class.csv')[['input', 'label']] \
                .dropna() \
                .reset_index()
cache.set('samples_200_per_class.csv', df)

df = pd.read_csv('demo/datasets/samples_500_per_class.csv')[['input', 'label']] \
                .dropna() \
                .reset_index()
cache.set('samples_500_per_class.csv', df)

cache.set('classification-files', ['samples_200_per_class.csv', 'samples_500_per_class.csv'])
cache.set('files', ['samples_200_per_class.csv', 'samples_500_per_class.csv'])
print("App started")