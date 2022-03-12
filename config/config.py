import os

MONGO_URI = 'mongodb://localhost:27017/test'
CACHE_TYPE = 'SimpleCache'
CACHE_DEFAULT_TIMEOUT = 0

def load_properties():
    global MONGO_URI

    if os.environ.get("PROFILE") == 'prod':
        MONGO_HOST = os.environ.get("MONGO_HOST")
        MONGO_PORT = os.environ.get("MONGO_PORT")
        MONGO_DB = os.environ.get("MONGO_DB")
        MONGO_URI = 'mongodb://{}:{}/{}'.format(MONGO_HOST, MONGO_PORT, MONGO_DB)


load_properties()