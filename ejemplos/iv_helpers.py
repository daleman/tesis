#! coding: utf-8
"""Helpers para las notebooks de Information Value."""
import nltk
from nltk.corpus import stopwords, gutenberg


def is_punctuation(c):
    u"""Devuelve True si c es un signo de puntuación."""
    is_simple = len(c) == 1 and c in "-.'?!,\":;()|-/"

    is_complex = c == '""' or c == '--' or c == ').' or c == '.""' or c == ''

    return is_simple or is_complex or len(c) == 1


def tokenize(text, only_alpha=False,
             only_alphanum=True, clean_stop_words=False,
             clean_punctuation=True):
    u"""Tokeniza text sacando algunos de ser necesario"""
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


def get_moby_dick_tokens():
    """Devuelve tokens de Moby Dick"""
    moby_dick = gutenberg.raw('melville-moby_dick.txt')
    tokens = tokenize(moby_dick, only_alphanum=True, clean_punctuation=True)
    return [token.lower() for token in tokens]
