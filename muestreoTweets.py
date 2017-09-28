from nltk.tokenize import TweetTokenizer
import unicodecsv
from apps import argentina
import pandas as pd
import datetime
import csv
from textos import cant_palabras
import json

path = '/home/dami/Desktop/datosTesis/train/train_'
path_listas = 'train/listas/'

def dictionary(provincia, completo):
    tknzr = TweetTokenizer(preserve_case=False,
                           reduce_len=True, strip_handles=True)
    dicc = {}
    dicc_usuarios = {}
    cant_words = 0
    file_path = path + provincia + '.csv'
    with open(file_path, 'r') as f:
        reader = unicodecsv.reader(
            f, encoding="utf-8", delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            # row[2] es la columna de texto
            if (completo):
                texto = [w for w in tknzr.tokenize(row[2].lower()) if w.isalpha()]
            else:
                texto = [w for w in tknzr.tokenize(
                    row[2]) if w.isalpha() and (not d.check(w))]
            uid = row[1]    # la columna de user id
            tid = row[0]

            for w in texto:
                #wl = w.lower()
                dicc[w] = 1 if not dicc.has_key(w) else dicc[w] + 1
                if dicc_usuarios.has_key(w):
                    if tid not in dicc_usuarios[w]:
                        dicc_usuarios[w][tid]=1
                    else:
                        dicc_usuarios[w][tid]+=1
                else:
                    dicc_usuarios[w] = {tid:1}
                # cant_words +1= 1
    return dicc, dicc_usuarios



def save_dicts(pais,completo):
    words = {}
    cant_words = {}
    dicc_usuarios = {}
    for prov in pais:
        cant_words[prov] = 0
    for prov in pais:
        start = datetime.datetime.now()
        words[prov], dicc_usuarios[prov] = dictionary(prov, completo)
        cant_words[prov] = cant_palabras(words[prov])
        end = datetime.datetime.now()
        with open(path + prov + '_dict_tweet.json', 'w') as fp:
            json.dump(words[prov], fp, encoding="utf-8")
        with open(path + prov + '_users_dict_tweet.json', 'w') as fp:
            json.dump(dicc_usuarios[prov], fp, encoding="utf-8")
        print prov, cant_words[prov], end - start
    return (words, cant_words, dicc_usuarios)


def load_dicts(pais):
    words = {}
    cant_words = {}
    dicc_usuarios = {}
    for prov in pais:
        cant_words[prov] = 0
    for prov in pais:
        print prov
        with open(path + prov + '_dict_tweet.json') as fi:
            words[prov] = json.load(fi)
        cant_words[prov] = cant_palabras(words[prov])
        with open(path + prov + '_users_dict_tweet.json') as fi:
            dicc_usuarios[prov] = json.load(fi)

    return (words, cant_words, dicc_usuarios)


""" Este script toma los diccionarios hechos por la funcion dictionary de textos.py y
 genera  archivos csv con la cantidad de ocurrencias de palabras por cada tweet.
"""

if __name__ == "__main__":

    wcd = save_dicts(argentina,True)

    #wcd = load_dicts(argentina)
    words = wcd[0]
    cant_words = wcd[1]
    dicc_usuarios = wcd[2]

    for p in argentina:
        df = pd.DataFrame.from_dict(dicc_usuarios[p],orient='index')
        #df = df.drop('user_id', 1)
        df.fillna(0,inplace=True)
        ser = df.sum(axis=0)
        df = df[df.sum(axis = 1) > 40]
        df = (df / ser)*1000000
        df.to_csv('./dataUsuarios/TRAINLABO/{0}.csv'.format(p),encoding='utf-8')