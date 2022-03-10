import pickle

import dash
import dash_bootstrap_components as dbc
import pandas as pd

from config.config import CACHE_TYPE, CACHE_DEFAULT_TIMEOUT, MONGO_URI
from config.cache import cache
from config.mongo import mongo

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME], suppress_callback_exceptions=True)

cache.init_app(app.server,
               config={
                   "DEBUG": True,
                   "CACHE_TYPE": CACHE_TYPE,
                   "CACHE_DEFAULT_TIMEOUT": CACHE_DEFAULT_TIMEOUT
               })

mongo.init_app(app.server, uri=MONGO_URI)

# Load initial data
cache.set('models', [])
cache.set('classification-models', [])

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
