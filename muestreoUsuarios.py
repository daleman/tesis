from apps import argentina
from textos import load_dicts
import pandas as pd
""" Este script toma los diccionarios hechos por la funcion dictionary de textos.py y
 genera .csv que tienen la cantidad de ocurrencias de las palabras por cada usuario.
"""
wcd = load_dicts(argentina)
words = wcd[0]
cant_words = wcd[1]
dicc_usuarios = wcd[2]

for p in argentina:
    df = pd.DataFrame.from_dict(dicc_usuarios[p],orient='index')
    df = df.drop('user_id', 1)
    df.fillna(0,inplace=True)
    ser = df.sum(axis=0)
    df = df[df.sum(axis = 1) > 40]
    df = (df / ser)*1000000
    df.to_csv('./dataUsuarios/{0}.csv'.format(p),encoding='utf-8')