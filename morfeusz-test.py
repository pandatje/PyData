# -*- coding: utf-8 -*-
from __future__ import print_function

from morfeusz2 import Morfeusz


def preprocess(text):
    return text.lower().replace('.', '').replace(',', '').replace('-', ' ')


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
        output.append(dictionary[word])
    return ' '.join(output)


if __name__ == '__main__':
    text = u'Sądy i Trybunały są władzą odrębną i niezależną od innych władz.'
    lemmatized = lemmatize(text)
    print(lemmatized)