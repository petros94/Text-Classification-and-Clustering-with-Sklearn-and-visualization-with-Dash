import base64
import io
import uuid

import pandas as pd

from config.cache import cache
from models.clustering import TextClustering
from services.text_preprocessing import generate_tfidf
from util import TextPreprocessor


@cache.memoize()
def generate_optimal_cluster_figures(filename):
    df = cache.get(filename)
    tfidf_vector, tfidf_matrix, dense = generate_tfidf(filename)
    tcl = TextClustering(df, tfidf_matrix, tfidf_vector, 12)
    sil_fig, sse_fig = tcl.find_optimal_clusters(20, debug=True, plot=False, fixed_size=False)
    return sil_fig, sse_fig

def evaluate_cluster(n_clusters, filename):
    df = cache.get(filename)
    tfidf_vector, tfidf_matrix, dense = generate_tfidf(filename)
    tcl = TextClustering(df, tfidf_matrix, tfidf_vector, n_clusters)
    clustered_data, fig = tcl.fit_kmeans(n_clusters, dash=True)

    top_terms = []

    for i in range(n_clusters):
        idx = clustered_data.pred == i
        print("Cluster {}".format(i))
        top_terms.append(clustered_data.loc[idx, ['input', 'top_terms']][0:5])

    plt_sil = tcl.plot_silhouette(plot=False)
    print("Calculated silhouette")
    buf = io.BytesIO()  # in-memory files
    plt_sil.savefig(buf, format="png")  # save to the above file object
    plt_sil.close()
    data = base64.b64encode(buf.getbuffer()).decode("utf8")  # encode to html elements
    img_sil = "data:image/png;base64,{}".format(data)

    random_id = "temp-" + str(uuid.uuid4())
    cache.set(random_id, tcl)

    return clustered_data, top_terms, fig, img_sil, random_id


def save_model(name, n_clusters, filename, temp_model_id):
    print("Entered save_model with args: {}, {}, {}".format(name, n_clusters, filename))
    tcl = cache.get(temp_model_id)

    models = cache.get('models')
    models.append(name)
    cache.set(name + "-model", tcl)
    cache.set('models', models)


def predict_text_cluster(model, text):
    print("Entered predict_text_cluster with args: {}, {}".format(model, text))
    tcl = cache.get(model + "-model")
    vb = tcl.tfidf_vector.vocabulary_

    tpr = TextPreprocessor(drop_common_words=False, vocabulary=vb)
    tfidf_vector, tfidf_matrix, dense = tpr.generate_tfidf(pd.Series([text]), fast=False)
    pred = tcl.predict(tfidf_matrix)[0]
    print(pred)

    idx = tcl.clustered_data.pred == pred
    print(idx)
    top_terms = tcl.clustered_data.loc[idx, 'top_terms'].iloc[0]
    print(top_terms)

    return pred, top_terms


