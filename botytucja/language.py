# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
import json
import string
from collections import OrderedDict

import gensim
import numpy as np
from morfeusz2 import Morfeusz
from nltk.tokenize import word_tokenize


def preprocess(text):
    return text.lower().replace('.', '').replace(',', '').replace('-', ' ').replace('"', '')


def lemmatize(text):
    text = preprocess(text)
    m = Morfeusz()
    results = m.analyse(text)
    dictionary = {}
    for line in results:
        index, token, (word, stub, _, _, _) = line
        word = word.encode('utf-8').lower()
        stub = stub.encode('utf-8').split(b':')[0].lower()
        if word not in dictionary.keys():
            dictionary[word] = stub

    output = []
    for word in text.split():
        word = word.encode('utf-8')
        output.append(dictionary.get(word, word))
    return ' '.join(output)


def tokenize_articles(articles):
    # table = string.maketrans({key: None for key in string.punctuation})
    gen_docs = [
        [w.lower() for w in word_tokenize(text.translate(None, string.punctuation))]
        for text in articles
    ]
    return gen_docs


def find_most_similar(text):
    with open('data/konstytucja.json', 'rt') as f:
        articles = json.loads(f.read())[u'artykuły']
    articles = OrderedDict(sorted(articles.items()))
    articles_lemmatized = [lemmatize(article) for article in list(articles.values())]
    gen_docs = tokenize_articles(articles_lemmatized)
    dictionary = gensim.corpora.Dictionary(gen_docs)

    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]

    tf_idf = gensim.models.TfidfModel(corpus)

    sims = gensim.similarities.Similarity('.', tf_idf[corpus], num_features=len(dictionary))

    text_lemmatized = lemmatize(text)
    query_doc = [w.lower() for w in word_tokenize(text_lemmatized)]
    query_doc_bow = dictionary.doc2bow(query_doc)
    query_doc_tf_idf = tf_idf[query_doc_bow]
    most_similar_index = np.argmax(sims[query_doc_tf_idf])
    article_key = str(most_similar_index+1).rjust(3, '0')
    return np.max(sims[query_doc_tf_idf]), articles[article_key]


if __name__ == '__main__':
    # query = sys.argv[1]
    # similarity, result = find_most_similar(query)
    # print(similarity, result)

    query = u'prezydent'
    print('looking for the most similar article to:')
    print(query.encode('utf-8'))
    print()
    similarity, article = find_most_similar(query)
    print('found (similarity %.2f):' % (similarity))
    print(article.encode('utf8'))
