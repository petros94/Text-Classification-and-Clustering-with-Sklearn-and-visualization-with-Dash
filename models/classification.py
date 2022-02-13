import time

from sklearn.naive_bayes import MultinomialNB

from util import import_data, TextPreprocessor


class TextClassification:
    def __init__(self):
        self.classifier = MultinomialNB()
        self.tpr = TextPreprocessor()

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