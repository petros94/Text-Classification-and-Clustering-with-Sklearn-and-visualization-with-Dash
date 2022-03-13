import os

MONGO_URI = 'mongodb://localhost:27017/test'
CACHE_TYPE = 'SimpleCache'
CACHE_DIR = None
CACHE_THRESHOLD = None
CACHE_DEFAULT_TIMEOUT = 3600

def load_properties():
    global MONGO_URI
    global CACHE_TYPE
    global CACHE_THRESHOLD
    global CACHE_DIR

    if os.environ.get("PROFILE") == 'docker':
        MONGO_HOST = os.environ.get("MONGO_HOST")
        MONGO_PORT = os.environ.get("MONGO_PORT")
        MONGO_DB = os.environ.get("MONGO_DB")
        MONGO_URI = 'mongodb://{}:{}/{}'.format(MONGO_HOST, MONGO_PORT, MONGO_DB)
        CACHE_TYPE = 'FileSystemCache'
        CACHE_THRESHOLD = 10
        CACHE_DIR = 'cache'

    elif os.environ.get("PROFILE") == 'prod':
        MONGO_URI = os.environ.get("MONGO_URI")
        CACHE_TYPE = 'FileSystemCache'
        CACHE_THRESHOLD = 10
        CACHE_DIR = 'cache'


load_properties()