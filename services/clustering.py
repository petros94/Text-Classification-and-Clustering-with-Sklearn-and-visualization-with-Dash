import base64
import io
import uuid

import pandas as pd

from config.cache import cache
from models.text_cluster import TextClustering, load_model, save_model as save
from services.preprocessing import generate_tfidf
from services.storage import find_clustering_doc_by_id


@cache.memoize()
def generate_optimal_cluster_figures(filename, common_words):
    df = find_clustering_doc_by_id(filename)['content']
    tcl = TextClustering(common_words=common_words)
    tcl.generate_tfidf(df.input)
    sil_fig, sse_fig = tcl.find_optimal_clusters(20, debug=True, plot=False, fixed_size=False)
    return sil_fig, sse_fig

def evaluate_cluster(n_clusters, doc_id, common_words):
    df = find_clustering_doc_by_id(doc_id)['content']
    tcl = TextClustering(cluster_size=n_clusters, common_words=common_words)
    clustered_data, fig = tcl.train(df.input, n_clusters)

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
    save(random_id, tcl, temp=True)

    return clustered_data, top_terms, fig, img_sil, random_id


def save_model(name, n_clusters, filename, temp_model_id, cluster_names):
    print("Entered save_model with args: {}, {}, {}, {}".format(name, n_clusters, filename, cluster_names))
    tcl = load_model(temp_model_id, temp=True)
    tcl.cluster_names = cluster_names
    print("loaded temp model")
    save(name, tcl, temp=False)


def predict_text_cluster(model, text):
    print("Entered predict_text_cluster with args: {}, {}".format(model, text))
    tcl = load_model(model, temp=False)
    pred = tcl.predict(pd.Series([text]))[0]
    print(pred)
    top_terms = tcl.top_terms[pred]
    cluster_name = tcl.cluster_names[pred]
    return pred, top_terms, cluster_name


