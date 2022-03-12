import pickle

from bson import Binary, ObjectId

from config.mongo import mongo
from config.cache import cache


# Models

def find_all_classifications_models():
    return mongo.db.tcfmodels.find({}, {"_id": 1, "name": 1})

def find_all_cluster_models():
    return mongo.db.tclmodels.find({}, {"_id": 1, "name": 1})

def load_classification_model(model_id, temp=False):
    if temp:
        saved = cache.get(model_id)
    else:
        saved = mongo.db.tcfmodels.find_one({'_id': ObjectId(model_id)})
    obj = pickle.loads(saved['data'])
    return obj


def save_classification_model(model_name, model_obj, temp=False):
    data = pickle.dumps(model_obj)
    if temp:
        cache.set(model_name, {'name': model_name, 'data': data})
    else:
        mongo.db.tcfmodels.insert_one({'name': model_name, 'data': Binary(data)})


def load_cluster_model(model_id, temp=False):
    if temp:
        saved = cache.get(model_id)
    else:
        saved = mongo.db.tclmodels.find_one({'_id': ObjectId(model_id)})
    obj = pickle.loads(saved['data'])
    return obj


def save_cluster_model(model_name, model_obj, temp=False):
    data = pickle.dumps(model_obj)
    if temp:
        cache.set(model_name, {'name': model_name, 'data': data})
    else:
        mongo.db.tclmodels.insert_one({'name': model_name, 'data': Binary(data)})


# Docs

def find_all_classification_docs():
    return mongo.db.tcfdocs.find({}, {"_id": 1, "filename": 1})


def find_all_cluster_docs():
    return mongo.db.tcldocs.find({}, {"_id": 1, "filename": 1})


def find_classification_doc_by_id(doc_id):
    doc = mongo.db.tcfdocs.find_one({"_id": ObjectId(doc_id)})
    return {'filename': doc['filename'], 'content': pickle.loads(doc['content'])}


def find_clustering_doc_by_id(doc_id):
    doc = mongo.db.tcldocs.find_one({"_id": ObjectId(doc_id)})
    return {'filename': doc['filename'], 'content': pickle.loads(doc['content'])}


def insert_classification_doc(filename, content):
    return mongo.db.tcfdocs.insert_one({'filename': filename, 'content': Binary(pickle.dumps(content))})


def insert_cluster_doc(filename, content):
    return mongo.db.tcldocs.insert_one({'filename': filename, 'content': Binary(pickle.dumps(content))})
