import sys
import json
import string

import gensim
import numpy as np
from nltk.tokenize import word_tokenize


def tokenize_articles(articles):
    table = str.maketrans({key: None for key in string.punctuation})
    gen_docs = [
        [w.lower() for w in word_tokenize(text.translate(table))]
        for text in articles
    ]
    return gen_docs


def find_most_similar(text):
    with open('data/konstytucja.json', 'rt') as f:
        articles = json.loads(f.read())['artykuły']
    articles = list(articles.values())
    gen_docs = tokenize_articles(articles)
    dictionary = gensim.corpora.Dictionary(gen_docs)
    # for i in range(len(dictionary)):
    #     print(i, dictionary[i])

    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
    # for doc in corpus:
    #     print(doc)
    #     for token, count in doc:
    #         print(dictionary[token], count)

    tf_idf = gensim.models.TfidfModel(corpus)
    # print(tf_idf)

    sims = gensim.similarities.Similarity('.', tf_idf[corpus], num_features=len(dictionary))
    # print(sims)
    # print(type(sims))

    query_doc = [w.lower() for w in word_tokenize(text)]
    query_doc_bow = dictionary.doc2bow(query_doc)
    query_doc_tf_idf = tf_idf[query_doc_bow]
    most_similar_index = np.argmax(sims[query_doc_tf_idf])
    return articles[most_similar_index]


if __name__ == '__main__':
    query = sys.argv[1]
    result = find_most_similar(query)
    print(result)
