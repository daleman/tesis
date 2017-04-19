# coding: utf-8
from textos import dictionary, cant_palabras, load_dicts
import enchant
import datetime
from apps import *
from nltk.tokenize import TweetTokenizer
import csv
import pandas as pd
import json
import re
import operator
import jellyfish


def save_dicts(pais, completo):
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
        print prov, cant_words[prov], end - start
    return (words, cant_words, dicc_usuarios)


def filtrarPalabras(df, cantUsuarios, cantOcurrencias):
    ''' Devuelve un Dataframe filtrando las palabras que tienen menos de cantUsuarios
    que la utilizan o con menos de cantOcurrencias. '''
    return (df[(df.cantUsuariosTotal > cantUsuarios) & (df.cantPalabra > cantOcurrencias)]).copy()


def risas(df):
    ''' Devuelve una lista de palabras que coinciden con risas como jaj, jej, jij, jejeje, jajaj, etc.'''
    i = 0
    sacar = []
    palabras = df.index
    jaregex = r'j+a[aj]+$|a+j[aj]+$'
    jeregex = r'j+e[ej]+$|e+j[ej]+$'
    jiregex = r'j+i[ij]+$|i+j[ij]+$'

    for palabra in palabras:
        if re.match(jaregex, palabra):
            # print palabra,i
            sacar.append(palabra)
            i += 1
        elif re.match(jeregex, palabra):
            # print palabra,i
            sacar.append(palabra)
            i += 1
        elif re.match(jiregex, palabra):
            # print palabra,i
            sacar.append(palabra)
            i += 1
    return sacar


def triPalabras(df):
    ''' Devuelve una lista de palabras que tienen tres ocurrencias de una misma letra.'''
    palabras = df.index
    i = 1
    tripalabras = []
    triregex = r'[a-z]+([a-z])\1{2}'
    for palabra in palabras:
        if re.match(triregex, palabra):
            print palabra, i
            tripalabras.append(palabra)
            i += 1
    return tripalabras


def triPalabrasASacar(triPalabras):
    i = 1
    sacar = []
    noPalabras = []
    d = enchant.Dict("es_AR")
    for pal in sorted(tripalabras):
        replaced = re.sub(r'([a-z])\1{2}', r'\1', pal)
        print pal
        if d.check(replaced):
            sacar.append(pal)
            print i, pal, replaced
            i += 1
        else:
            noPalabras.append(pal)
    print i, len(tripalabras)
    return sacar


def indicesTildes(palabra):
    vowels = ['a', 'e', 'i', 'o', 'u']
    index_vowels = []
    for i in range(len(palabra)):
        if palabra[i] in vowels:
            index_vowels.append(i)
    return index_vowels


def cambiarLetraTilde(letra):
    conTilde = {'a': 'á', 'e': 'é', 'i': 'í', 'o': 'ó', 'u': 'ú'}
    return conTilde[letra]


def cambiarPalabraTilde(palabra, indice):
    prefijo = palabra[0:indice]
    letraTilde = cambiarLetraTilde(palabra[indice])
    sufijo = palabra[indice + 1:]
    return prefijo + letraTilde + sufijo


def damePalabrasTildes(palabra):
    indices = indicesTildes(palabra)
    palabras = []
    for i in indices:
        palTilde = cambiarPalabraTilde(palabra, i)
        palabras.append(palTilde)
    return palabras


def palabrasRepetidas(df):
    d = enchant.Dict("es_AR")
    palabras = df.index
    i = 1
    palabrasRepetidas = []
    repRegex = r'[a-z]*([a-z])\1{1,}.*'
    for palabra in palabras:
        if re.match(repRegex, palabra):
            replaced = re.sub(r'([a-z])\1{1,}', r'\1', palabra)
            palabrasRepetidas.append(palabra)
            if (d.check(replaced)):
                print palabra, replaced, i
                i += 1
    return palabrasRepetidas


def diccSugerencias(df):
    similarity = jellyfish.jaro_winkler
    THRESHOLD = 0.85
    palabras = df.index
    sugerencias = {}

    """
    Para cada par de palabras p1, p2:
        Si sim(p1, p2) > THRESHOLD:
            sugiero p2 para p1

    """
    for i in range(len(palabras)):
        p1 = palabras[i]

        palabras_cercanas = []

        for j in range(i + 1, len(palabras)):
            p2 = palabras[j]

            sim = similarity(p1.decode("utf-8"), p2.decode("utf-8"))
            if sim > THRESHOLD:
                palabras_cercanas.append((p2, sim))

        # Las ordeno en orden decreciente de similaridad
        palabras_cercanas = sorted(
            palabras_cercanas, key=operator.itemgetter(1), reverse=True)
        sugerencias[p1] = [p[0] for p in palabras_cercanas]
        # Para no atestar el output, sólo imprimo cada 250
        if i % 250 == 0:
            print("{} --> recomendadas : {}".format(p1, palabras_cercanas))
    return sugerencias


def sugerencias_a_string(palabra, sugerencias):
    sug = sugerencias[palabra]
    return u",".join(s.decode("utf-8") for s in sug)


def agregarSugerencias(df):
    sugerencias = diccSugerencias(df)
    df['sugerencias'] = map(
        lambda p: sugerencias_a_string(p, sugerencias), df.index)
    # df[["Palabra", "sugerencias"]].to_csv("palabras_y_sugerencias.csv",
    # encoding="utf-8")


if __name__ == "__main__":

    path = 'train/train_'

    wcd = load_dicts(argentina)  # save_dicts(argentina, True)
    words = wcd[0]
    cant_words = wcd[1]
    dicc_usuarios = wcd[2]

    cantPorProvincia = {prov: sum(words[prov].values()) for prov in argentina}

    users_cant = {}
    for prov in argentina:
        for pal, lista in dicc_usuarios[prov].iteritems():
            # print prov,pal,lista
            if not users_cant.has_key(prov):
                users_cant[prov] = {}
                users_cant[prov][pal] = len(lista)
            else:
                users_cant[prov][pal] = len(lista)
    df = pd.DataFrame(words)
    df1 = pd.DataFrame(users_cant)
    print df.shape
    print df1.shape
    df = df.fillna(0)
    df1 = df1.fillna(0)
    df.columns = [str(col) + 'Palabras' for col in df.columns]
    df1.columns = [str(col) + 'Personas' for col in df.columns]
    df1['cantUsuariosTotal'] = df1.sum(axis=1)
    df['cantPalabra'] = df.sum(axis=1)

    result = pd.concat([df, df1], axis=1)

    for prov in argentina:
        result['fnorm_' + prov] = result[prov + 'Palabras'] / \
            (cantPorProvincia[prov] / 1000000.0)

    df_resultado = filtrarPalabras(
        df=result, cantUsuarios=5, cantOcurrencias=40)

    listaRisas = risas(df_resultado)
    # listaPalabrasConLetrasRepetidas = palabrasRepetidas(df_resultado)
    palabrasASacar = listaRisas  # + listaPalabrasConLetrasRepetidas
    # print 'La cantidad de palabras a sacar es ', len(palabrasASacar)
    dfRes = df_resultado[-df_resultado.index.isin(palabrasASacar)].copy()
    # print df_resultado.shape[0], dfRes.shape[0]

    # Le agrego la columna de MaxDif

    dfRes['cantProvinciasSinEsaPalabra'] = dfRes.filter(
        regex=("fnorm.*")).apply(lambda s: s.value_counts().get(0, 0), axis=1)
    idmax = dfRes.filter(regex=("fnorm.*")).idxmax(1)
    maxi = dfRes.filter(regex=("fnorm.*")).max(1)
    dfRes['provFnormMax'] = idmax
    dfRes['FnormMax'] = maxi
    idmin = dfRes.filter(
        regex=("fnorm.*"))[dfRes > 0.0000000000000001].idxmin(1)
    mini = dfRes.filter(
        regex=("fnorm.*"))[dfRes > 0.0000000000000001].min(1)
    dfRes['provFnormMin'] = idmin
    dfRes['FnormMin'] = mini

    # print dfRes.columns
    # minFnorm=dfRes['FnormMin'].min()
    # print minFnorm
    dfRes['maxDif'] = dfRes.FnormMax / dfRes.FnormMin

    dfRes[['provFnormMin', 'provFnormMax']] = dfRes[['provFnormMin',
                                                     'provFnormMax']].replace(to_replace='fnorm_', value='', regex=True)

    dfResumida = dfRes[['FnormMin', 'FnormMax', 'provFnormMin', 'provFnormMax',
                        'cantProvinciasSinEsaPalabra', 'maxDif']].sort_values(by=['maxDif', 'cantProvinciasSinEsaPalabra'], axis=0, ascending=[False, False], inplace=False)
    dfResumida.to_excel('contrastePalabrasResumido.xlsx')
    # agregarSugerencias(dfRes)
    dfRes.to_excel('contrasteExtendido.xlsx')
