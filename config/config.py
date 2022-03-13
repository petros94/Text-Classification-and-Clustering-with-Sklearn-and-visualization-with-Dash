import os

MONGO_URI = 'mongodb+srv://mltextapp:mltextapp@test-cluster.3l1bm.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
CACHE_TYPE = 'SimpleCache'
CACHE_DEFAULT_TIMEOUT = 3600

def load_properties():
    global MONGO_URI

    if os.environ.get("PROFILE") == 'docker':
        MONGO_HOST = os.environ.get("MONGO_HOST")
        MONGO_PORT = os.environ.get("MONGO_PORT")
        MONGO_DB = os.environ.get("MONGO_DB")
        MONGO_URI = 'mongodb://{}:{}/{}'.format(MONGO_HOST, MONGO_PORT, MONGO_DB)
    elif os.environ.get("PROFILE") == 'prod':
        MONGO_URI = os.environ.get("MONGO_URI")


load_properties()