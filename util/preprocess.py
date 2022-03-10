import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import string
from spacy.lang.en.stop_words import STOP_WORDS


class TextPreprocessor:
    def  __init__(self, drop_common_words=False, vocabulary=None):
        self.punctuations = string.punctuation
        self.stop_words = spacy.lang.en.stop_words.STOP_WORDS
        self.nlp = spacy.load('en_core_web_sm')

        self.tfidf_matrix = None
        self.tfidf_transformer = None
        self.dense_tfidf_matrix = None
        self.drop_common_words = drop_common_words
        self.vocabulary = vocabulary

    # Creating our tokenizer function
    def spacy_tokenizer(self, sentence):
        mytokens = self.nlp(sentence)

        # Lemmatizing each token and converting each token into lowercase
        filtered = filter(lambda it: it.lemma_.isalpha(), mytokens) \
            if not self.drop_common_words \
            else filter(lambda it: it.lemma_.isalpha() and it.lemma_.lower() not in ['buy', 'like', 'love', 'perfect', 'good', 'great', 'nice', 'excellent'], mytokens)
        mytokens = list(map(lambda it: it.lemma_.lower().strip(), filtered))

        # Removing stop words
        mytokens = [word for word in mytokens if word not in self.stop_words and word not in self.punctuations]

        # return preprocessed list of tokens
        return mytokens

    def generate_tfidf(self, text_data, max_features=None, debug=False, fast=True, dense=True):
        tfidf_transformer = TfidfVectorizer(tokenizer=self.spacy_tokenizer,
                                            max_features=max_features,
                                            vocabulary=self.vocabulary)
        if debug:
            print("Created tfidf transformer")

        if fast:
            tfidf_matrix = tfidf_transformer.fit_transform(text_data.to_list())
        else:
            tfidf_transformer.fit(text_data.to_list())
            tfidf_matrix = tfidf_transformer.transform(text_data.to_list())

        if debug:
            print("Created tfidf matrix")

        if dense:
            dense_tfidf_matrix = pd.DataFrame(tfidf_matrix.todense().tolist(),
                                              columns=tfidf_transformer.get_feature_names_out())
            self.dense_tfidf_matrix = dense_tfidf_matrix

            if debug:
                print("Created tfidf dense matrix")

        self.tfidf_transformer = tfidf_transformer
        self.tfidf_matrix = tfidf_matrix
        self.vocabulary = tfidf_transformer.vocabulary_
        return self.tfidf_transformer, self.tfidf_matrix, self.dense_tfidf_matrix



