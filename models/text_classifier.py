import pickle
import time

from sklearn.naive_bayes import MultinomialNB

from services.storage import load_classification_model as load
from services.storage import save_classification_model as save
from util import TextPreprocessor

class TextClassifier:
    def __init__(self, classifier=None, vocabulary=None):
        self.classifier = classifier if classifier is not None else MultinomialNB()
        self.tpr = TextPreprocessor(vocabulary=vocabulary)

    def train(self, raw_text, labels):
        start = time.time()
        tfidf_vector, tfidf_matrix, _ = self.tpr.generate_tfidf(raw_text, debug=False, dense=False)
        self.classifier.fit(tfidf_matrix, labels)
        return tfidf_matrix.shape[1], time.time() - start

    def predict(self, raw_text, prob=False):
        start = time.time()
        vb = self.tpr.vocabulary
        tpr = TextPreprocessor(vocabulary=vb)
        tfidf_vector, tfidf_matrix, _ = tpr.generate_tfidf(raw_text, debug=False, dense=False)
        return {'label': self.classifier.classes_, 'pred': self.classifier.predict_proba(tfidf_matrix)[0]} if prob else self.classifier.predict(tfidf_matrix), time.time() - start

    def accuracy_score(self, raw_text, labels):
        vb = self.tpr.vocabulary
        tpr = TextPreprocessor(vocabulary=vb)
        tfidf_vector, tfidf_matrix, _ = tpr.generate_tfidf(raw_text, debug=False, dense=False)
        return self.classifier.score(tfidf_matrix, labels)


def load_model(model_name, temp):
    obj = load(model_name, temp=temp)
    clf = obj['classifier']
    voc = obj['vocabulary']
    return TextClassifier(classifier=clf, vocabulary=voc)

def save_model(model_name, clf, temp):
    obj = {'classifier': clf.classifier, 'vocabulary': clf.tpr.vocabulary}
    save(model_name, obj, temp=temp)