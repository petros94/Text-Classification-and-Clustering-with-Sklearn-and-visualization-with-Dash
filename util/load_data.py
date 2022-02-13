import random

import pandas as pd

def import_data(path, size, file_type, field, label=None):
    if file_type == 'json':
        data = pd.read_json(path, lines=True, nrows=size)[[field]]
    elif file_type == 'csv':
        data = pd.read_csv(path, nrows=size)[[field]]
    else:
        raise ValueError("Invalid file_type")

    if label:
        data['label'] = label

    return data.rename(columns={field: 'input'}).dropna()