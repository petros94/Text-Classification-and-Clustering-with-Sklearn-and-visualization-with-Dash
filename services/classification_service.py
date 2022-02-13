import base64
import io
import uuid

import pandas as pd
import plotly.express as px
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix
from sklearn.model_selection import train_test_split

from config.cache import cache
from models.classification import TextClassification
from models.clustering import TextClustering
from services.text_preprocessing import generate_tfidf
from util import TextPreprocessor


def evaluate_classifier(filename):
    df = cache.get(filename)
    tcf = TextClassification()
    X_train, X_test, y_train, y_test = train_test_split(df.input, df.label, test_size=0.2)
    print("Training model")
    n_features, training_time = tcf.train(X_train, y_train)
    print("Training complete")

    labels = df.label.factorize()[1].to_list()

    print("Evaluation of test set")
    y_pred, pred_time = tcf.predict(X_test)
    acc = tcf.accuracy_score(X_test, y_test)
    pre, rec, f1, sup = precision_recall_fscore_support(y_test, y_pred, labels=labels)
    metrics_exp_0 = pd.DataFrame({'Accuracy': [acc] * 5,
                                  'Precision': pre,
                                  'Recall': rec,
                                  'F1': f1,
                                  'Label': labels})


    cm = confusion_matrix(y_test, y_pred, labels=labels)
    df_cm = pd.DataFrame(cm, columns=labels, index=labels)
    random_id = "temp-" + str(uuid.uuid4())
    cache.set(random_id, tcf)

    svd = TruncatedSVD(n_components=5)
    vb = tcf.tpr.vocabulary
    tpr = TextPreprocessor(vocabulary=vb)
    tfidf_vector, tfidf_matrix, _ = tpr.generate_tfidf(X_test, debug=False, dense=False)
    Y = svd.fit_transform(tfidf_matrix)

    fig3 = px.scatter(x=Y[:, 2], y=Y[:, 4], color=[v if v == u else 'incorrect class' for v, u in zip(y_test, y_pred)])
    fig4 = px.scatter(x=Y[:, 4], y=Y[:, 3], color=[v if v == u else 'incorrect class' for v, u in zip(y_test, y_pred)])

    return n_features, training_time, metrics_exp_0, df_cm, random_id, fig3, fig4


def save_model(name, temp_model_id):
    print("Entered save_model with args: {}, {}".format(name, temp_model_id))
    tcf = cache.get(temp_model_id)

    models = cache.get('classification-models')
    models.append(name)
    cache.set(name + "-model", tcf)
    cache.set('classification-models', models)


def predict_text_label(model, text):
    print("Entered predict_text_label with args: {}, {}".format(model, text))
    tcf = cache.get(model + "-model")
    return tcf.predict(pd.Series([text]), prob=True)



