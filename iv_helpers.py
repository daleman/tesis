#! coding: utf-8
"""Helpers para las notebooks de Information Value."""
import nltk
import json
from scipy.stats import entropy
from nltk.corpus import stopwords, gutenberg
from numpy.random import multinomial
from nltk import word_tokenize


def lugares():
    with open('../localidades/cabeceras.geojson') as cab,\
            open('../localidades/capitales.geojson') as cap,\
            open('../localidades/localidades.geojson') as loc,\
            open('../localidades/departamentos.geojson') as dep:
        cabeceras = json.load(cab)
        capitales = json.load(cap)
        localidades = json.load(loc)
        departamentos = json.load(dep)
        lugares = set([])
        for a in [cabeceras, capitales, localidades, departamentos]:
            for n in a['features']:
                for w in nltk.word_tokenize(n['properties']['nombre']):
                    lugares.add(w.lower())

    return lugares


def shuffle(balls, bins):
    return multinomial(balls, [1. / bins] * bins)


def is_punctuation(c):
    u"""Devuelve True si c es un signo de puntuación."""
    is_simple = len(c) == 1 and c in "-.'?!,\":;()|-/"

    is_complex = c == '""' or c == '--' or c == ').' or c == '.""' or c == ''

    return is_simple or is_complex or len(c) == 1


def tokenize(text, only_alpha=False,
             only_alphanum=True, clean_stop_words=False,
             clean_punctuation=True):
    u"""Tokeniza text sacando algunos de ser necesario."""
    tokens = nltk.wordpunct_tokenize(text)

    def accept_token(t):
        not_punctuation = not (clean_punctuation and is_punctuation(t))
        alpha = not only_alpha or t.isalpha()
        alnum = not only_alphanum or t.isalnum()
        not_stopword = not clean_stop_words or \
            t not in stopwords.words('english')
        return not_punctuation and alpha and alnum and not_stopword

    tokens = [t for t in tokens if accept_token(t)]
    return tokens

import random


def random_balls_in_bins(balls, bins):
    """Return a list of <bins> integers that sum <balls>.

    We can think this as a problem of bosons:

    We have to distribute balls in bins. To model this, we use a shuffle of

    'o' * balls + '|' * (bins-1)

    This results in a string of the form oo|ooo|oo where we leave the last '|' fixed

    Parameters:
    ----------

    balls: int > 0
        number of balls to distribute
    bins: int > 0
        number of bins

    Returns
    -------

    A list of <bins> integers that sum <balls>
    """
    balls_and_bins = list('o' * balls + '|' * (bins - 1))
    random.shuffle(balls_and_bins)

    bins = []
    current = 0

    for e in balls_and_bins:
        if e == 'o':
            current += 1
        elif e == '|':
            bins.append(current)
            current = 0

    bins.append(current)

    return bins


def simulated_shuffled_entropy(n, p):
    """Calculate simulated-shuffled entropy.

    Parameters
    ----------

    n: int
        Number of occurrences of word
    p: int
        Number of parts in text
    """
    shuffled_words = random_balls_in_bins(balls=n, bins=p)
    assert(sum(shuffled_words) == n)
    return entropy(shuffled_words)


def simulated_shuffled_entropy_multinomial(n, p):
    """Calculate simulated-shuffled entropy.

    Parameters
    ----------

    n: int
        Number of occurrences of word
    p: int
        Number of parts in text
    """
    shuffled_words = shuffle(balls=n, bins=p)
    assert(sum(shuffled_words) == n)
    return entropy(shuffled_words)


def get_moby_dick_tokens():
    """Devuelve tokens de Moby Dick."""
    moby_dick = gutenberg.raw('melville-moby_dick.txt')
    tokens = tokenize(moby_dick, only_alphanum=True, clean_punctuation=True)
    return [token.lower() for token in tokens]
