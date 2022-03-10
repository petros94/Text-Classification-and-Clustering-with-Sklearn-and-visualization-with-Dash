import base64
import io
import pickle
import uuid

import pandas as pd
import plotly.express as px
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix
from sklearn.model_selection import train_test_split

from models.text_classifier import TextClassifier, save_model as save, load_model as load
from services.storage import find_classification_doc_by_id
from util import TextPreprocessor


def train_evaluate(doc_id):
    df = find_classification_doc_by_id(doc_id)['content']
    tcf = TextClassifier()
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
    save(random_id, tcf, temp=True)

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
    tcf = load(temp_model_id, temp=True)
    print("loaded temp model: ", tcf)
    save(name, tcf, temp=False)


def predict_text_label(model_id, text):
    print("Entered predict_text_label with args: {}, {}".format(model_id, text))
    tcf = load(model_id, temp=False)
    return tcf.predict(pd.Series([text]), prob=True)



