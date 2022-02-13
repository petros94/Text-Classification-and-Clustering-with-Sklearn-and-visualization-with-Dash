from config.cache import cache
from util import TextPreprocessor

@cache.memoize()
def generate_tfidf(filename):
    print("Generating tfidf")
    tpr = TextPreprocessor(drop_common_words=False)
    df = cache.get(filename)
    return tpr.generate_tfidf(df.input, debug=True, fast=False)