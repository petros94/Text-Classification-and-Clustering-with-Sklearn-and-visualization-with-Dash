import time

import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import pandas as pd
from matplotlib import cm
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
from services.storage import load_cluster_model as load
from services.storage import save_cluster_model as save
from util import TextPreprocessor

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)

class TextClustering:
    def __init__(self, model=None, vocabulary=None, common_words=None, cluster_size=6, top_terms=None, cluster_names=None, clustered_data=None):
        self.cluster_size = cluster_size
        self.kmeans = model
        self.clustered_data = clustered_data
        self.tpr = TextPreprocessor(vocabulary=vocabulary, drop_common_words=common_words)
        self.top_terms = top_terms
        self.cluster_names = cluster_names

    def predict(self, raw_text):
        vb = self.tpr.vocabulary
        tpr = TextPreprocessor(vocabulary=vb)
        tfidf_vector, tfidf_matrix, _ = tpr.generate_tfidf(raw_text, debug=False, dense=False)
        return self.kmeans.predict(tfidf_matrix)

    def generate_tfidf(self, raw_text):
        tfidf_vector, tfidf_matrix, _ = self.tpr.generate_tfidf(raw_text, debug=False, dense=False)

    def train(self, raw_text, cluster_size, skip_tfidf=False):
        if not skip_tfidf:
            tfidf_vector, tfidf_matrix, _ = self.tpr.generate_tfidf(raw_text, debug=False, dense=False)
        return self.fit_kmeans(raw_text, cluster_size, dash=True)

    def fit_kmeans(self, raw_text, cluster_size, plot=True, debug=False, dash=False):
        self.cluster_size = cluster_size
        self.kmeans = KMeans(n_clusters=self.cluster_size).fit(self.tpr.tfidf_matrix)
        pred = self.kmeans.predict(self.tpr.tfidf_matrix)

        self.clustered_data = pd.DataFrame({'input': raw_text}).join(pd.DataFrame({'pred': pred}))

        total = self.clustered_data.groupby("pred").size()
        self.clustered_data = self.clustered_data.join(
            pd.DataFrame({'total_in_group': self.clustered_data.apply(lambda row: total[row['pred']], axis=1).to_list()}))

        self.top_terms = self.top_terms_per_cluster(debug=debug)
        self.clustered_data = self.clustered_data.join(
            pd.DataFrame({"top_terms": self.clustered_data.apply(lambda row: self.top_terms[row["pred"]], axis=1).to_list()}))

        if plot and not dash:
            fig = px.bar(total.sort_values(), width=400, height=400)
            fig.show()
        elif plot and dash:
            fig = px.bar(total.sort_values())
            return self.clustered_data, fig


        return self.clustered_data

    def find_optimal_clusters(self, max_k, runs = 1, debug=False, plot=True, fixed_size=True):
        iters = range(2, max_k + 1, 1)

        sse = [0]*len(iters)
        sil_score = [0]*len(iters)
        for n in range(runs):
            for k in iters:
                kmeans = KMeans(n_clusters=k).fit(self.tpr.tfidf_matrix)
                pred = kmeans.predict(self.tpr.tfidf_matrix)
                sil_score[k-2] += silhouette_score(self.tpr.tfidf_matrix, pred)/runs
                sse[k-2] += kmeans.inertia_/runs
                if debug:
                    print('Fit {} clusters'.format(k))

        if fixed_size:
            sil_fig = px.scatter(x=iters, y=sil_score, width=400, height=400,
                                 labels={
                                     "x": "Number of clusters",
                                     "y": "Score"
                                 }, title=" Mean Silhouette Score")
            sse_fig = px.scatter(x=iters, y=sse, width=400, height=400,
                                 labels={
                                     "x": "Number of clusters",
                                     "y": "Score"
                                 }
                                 , title="Mean SSE Score")
        else:
            sil_fig = px.scatter(x=iters, y=sil_score,
                                 labels={
                                     "x": "Number of clusters",
                                     "y": "Score"
                                 }, title=" Mean Silhouette Score")
            sse_fig = px.scatter(x=iters, y=sse,
                                 labels={
                                     "x": "Number of clusters",
                                     "y": "Score"
                                 }
                                 , title="Mean SSE Score")
        if plot:
            sil_fig.show()
            sse_fig.show()
        return sil_fig, sse_fig

    def top_terms_per_cluster(self, debug):
        if debug:
            print("Top terms per cluster:")
        output = dict()
        order_centroids = self.kmeans.cluster_centers_.argsort()[:, ::-1]
        terms = self.tpr.tfidf_transformer.get_feature_names()
        for i in range(self.kmeans.n_clusters):
            if debug:
                print("Cluster %d:" % i, end='')
            temp = []
            for ind in order_centroids[i, :3]:
                if debug:
                    print(' %s' % terms[ind], end='')
                    print()
                temp.append(terms[ind] + "\n")
            output[i] = temp
        return output

    def plot_silhouette(self, plot=True):
        dense_tfidf_matrix = self.tpr.tfidf_matrix.todense()
        for n_clusters in [self.cluster_size]:
            # Create a subplot with 1 row and 1 columns
            fig, ax1 = plt.subplots(1, 1)
            fig.set_size_inches(18, 7)

            # The 1st subplot is the silhouette plot
            # The silhouette coefficient can range from -1, 1 but in this example all
            # lie within [-0.1, 1]
            ax1.set_xlim([-0.1, 1])
            # The (n_clusters+1)*10 is for inserting blank space between silhouette
            # plots of individual clusters, to demarcate them clearly.
            ax1.set_ylim([0, len(dense_tfidf_matrix) + (n_clusters + 1) * 10])

            cluster_labels = self.clustered_data.pred

            # The silhouette_score gives the average value for all the samples.
            # This gives a perspective into the density and separation of the formed
            # clusters
            silhouette_avg = silhouette_score(dense_tfidf_matrix, self.clustered_data.pred)
            print(
                "For n_clusters =",
                n_clusters,
                "The average silhouette_score is :",
                silhouette_avg,
            )

            # Compute the silhouette scores for each sample
            sample_silhouette_values = silhouette_samples(dense_tfidf_matrix, cluster_labels)

            y_lower = 10
            for i in range(self.cluster_size):
                # Aggregate the silhouette scores for samples belonging to
                # cluster i, and sort them
                ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]

                ith_cluster_silhouette_values.sort()

                size_cluster_i = ith_cluster_silhouette_values.shape[0]
                y_upper = y_lower + size_cluster_i

                color = cm.nipy_spectral(float(i) / n_clusters)
                ax1.fill_betweenx(
                    np.arange(y_lower, y_upper),
                    0,
                    ith_cluster_silhouette_values,
                    facecolor=color,
                    edgecolor=color,
                    alpha=0.7,
                )

                # Label the silhouette plots with their cluster numbers at the middle
                ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

                # Compute the new y_lower for next plot
                y_lower = y_upper + 10  # 10 for the 0 samples

            ax1.set_title("The silhouette plot for the various clusters.")
            ax1.set_xlabel("The silhouette coefficient values")
            ax1.set_ylabel("Cluster label")

            # The vertical line for average silhouette score of all the values
            ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

            ax1.set_yticks([])  # Clear the yaxis labels / ticks
            ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

            # Labeling the clusters
            centers = self.kmeans.cluster_centers_

            plt.suptitle(
                "Silhouette analysis for KMeans clustering on sample data with n_clusters = %d"
                % n_clusters,
                fontsize=14,
                fontweight="bold",
            )

        if plot:
            plt.show()
        return plt

def load_model(model_name, temp):
    obj = load(model_name, temp=temp)
    cls = obj['clustering']
    voc = obj['vocabulary']
    terms = obj['terms']
    names = obj['names']
    clustered_data = obj['data']
    return TextClustering(model=cls, vocabulary=voc, top_terms=terms, cluster_names=names, clustered_data=clustered_data)

def save_model(model_name, clf, temp):
    obj = {
        'clustering': clf.kmeans,
        'vocabulary': clf.tpr.vocabulary,
        'terms': clf.top_terms,
        'names': clf.cluster_names,
        'data': clf.clustered_data if temp else None
    }
    save(model_name, obj, temp=temp)