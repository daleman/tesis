# coding: utf-8
import json
from apps import *
import matplotlib.pyplot as plt
import numpy as np
import re
from nltk import word_tokenize
from string import punctuation
import sys

import statsmodels.api as sm
import statsmodels.stats as sta
import itertools
import datetime
import math

reload(sys)
sys.setdefaultencoding('utf-8')

path = 'tweetsFinal/pares/' 

#grep -wio 'independiente' ../impares/buenosaires_tokens.txt | wc -l



def plot(canti,dic):
    plt.title("Frecuencia de Palabras")
    plt.xlabel("Palabras")
    plt.ylabel("Frecuencia")

    index = np.arange(len(dic.keys()))
    bar_width = 0.35


    cant = canti
    valores = sorted(dic.values(),reverse=True)
    claves = sorted(dic, key=dic.get,reverse=True)

    opacity = 0.4
    plt.xticks(index + bar_width, claves[:cant], size=6, rotation="vertical")
    plt.bar(range(cant),valores[:cant],alpha=opacity,color='b',)
    plt.tight_layout()
    plt.show()


def dictionary(provincia):
    dicc = {}
    cant_words = 0
    #file_path = 'tweets2/' + provincia + '_tweets.json'
    file_path = path + provincia + '_tweets.json'
    with open(file_path) as f:
        for line in f:
            content = json.loads(line)
            texto =  content['text']
            texto = tokenize(texto)
            
            #texto = json.loads(line)
            for w in texto:
                wl = w.lower()
                dicc[wl] = 1 if not dicc.has_key(wl) else dicc[wl] +1
                # cant_words += 1
    return dicc

def remove_words(dicc,thresh):
    n_dict = { k:v for k, v in dicc.items() if v > thresh }
    return n_dict

def cant_palabras(dicc):
    return sum(dicc.values())

def fnorm(provincia,word,words,cant_words):
    if words[provincia].has_key(word):
        n = float(words[provincia][word])
    else:
        n = 0.0

    #if word == 'un' and (provincia =='buenosaires' or provincia =='cordoba'):
    #    print word,provincia,n,cant_words[provincia],n /(float(cant_words[provincia])/1000000)
    return n /(float(cant_words[provincia])/1000000)

def mean(provincia,word):
    return words[provincia][word]/float(cant_words[provincia])

def save_texts(provincia):
    file_path = provi + '_textos.json'
    file_w =  provi + '_solo_texto.json'
    with open(file_path) as f:
        for line in f:
            content = json.loads(line)
            texto =  content['text']
            with open(file_w,'a') as fi:
                fi.write(texto)
                fi.write('\n')
    return words

def tokenize(texto):
    #import ipdb; ipdb.set_trace()
    #print m
    texto = re.sub('@[\wáéíóú]*', '', texto)
    texto = re.sub('#[\wáéíóú]*', '', texto)
    texto = re.sub(r'http\S+', '', texto)
    texto = re.findall('[^\W\d]+', texto, re.UNICODE)
    texto =' '.join(texto)
    tokens =  word_tokenize(texto)
    return tokens

def ztest(x1,x2,n1,n2):
    from numpy import sqrt
    p1 = float(x1)/n1
    p2 = float(x2)/n2
    p = float(x1 + x2) / (n1 + n2)
    den = sqrt((p*(1.0-p)* ((1/float(n1))+(1/float(n2)))))
    z = (p1-p2) / den 
    return z 

def pvalor(z):
    import scipy.stats as st
    nz = z 
    if z > 0:
        nz = -z
    return 2*st.norm.cdf(nz)

def save_dicts(pais):
    words = {}
    cant_words = {}
    for prov in pais:
        cant_words[prov] = 0
    for prov in pais:
        start = datetime.datetime.now()
        #words[prov],cant_words[prov] = dictionary(prov)
        words[prov] = dictionary(prov)
        #n_dicc = remove_words(dicc,1)
        #words[prov] = n_dicc
        cant_words[prov] = cant_palabras(words[prov])
        end = datetime.datetime.now()
        with open(path + prov + '_dict.json', 'w') as fp:
            json.dump(words[prov], fp)
        print prov,cant_words[prov], end - start

def load_dicts(pais):    
    words = {}
    cant_words = {}
    for prov in pais:
        cant_words[prov] = 0
    for prov in pais:
        print prov
        with open(path+prov+'_dict.json') as fi:
            words[prov] = json.load(fi)
        for w in words[prov]:
            cant_words[prov] += words[prov][w]
    return words,cant_words

def save_list_words(pvalores,words,cant_words,p1,p2):
    import csv
    
    with open('tweetsFinal/listas/lista10317/' + str(p1) + '_' + str(p2) + '.csv','a') as fi:
        csvwriter = csv.writer(fi, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(('Palabra','cant P1' ,'cant P2' , 'Pvalue' ,'fnorm1' ,'fnorm2'))
        for w in sorted(pvalores,key=pvalores.get):
            cant_p1 = str(0.0) if not(words[p1].has_key(w)) else str(words[p1][w])
            cant_p2 = str(0.0) if not(words[p2].has_key(w)) else str(words[p2][w])
            fnorm1 = str(fnorm(p1,w,words,cant_words))
            fnorm2 = str(fnorm(p2,w,words,cant_words)) 
            #fi.write(w.encode('utf-8')+ "\t" + cant_p1  + '\t' + cant_p2 + '\t' +  str(pvalores[w]) + '\t' + fnorm1 + '\t' + fnorm2 + '\n')
            csvwriter.writerow((w.encode('utf-8'),cant_p1 ,cant_p2 ,str(pvalores[w]) ,fnorm1 ,fnorm2))
          

def test_par_provincias(words,cant_words,pais):
    import statsmodels.api as sm
    pvalores = {}
    for pair in itertools.combinations(pais, 2):
        start = datetime.datetime.now()
        p1 = pair[0]
        p2 = pair[1]
        for w in set(words[p1].keys()+words[p2].keys()):
            n1 = float(cant_words[p1])
            n2 = float(cant_words[p2])
            X1 = 0.0 if not(words[p1].has_key(w)) else words[p1][w]
            X2 = 0.0 if not(words[p2].has_key(w)) else words[p2][w]
            z_score, p_value = sm.stats.proportions_ztest([X1, X2], [n1, n2])
            pvalores[w] = p_value
        save_list_words(pvalores,words,cant_words,p1,p2)
        pvalores = {}
        end = datetime.datetime.now()
        print p1,p2, end - start

def test_par_provincias_bonfarroni(pais,words,cant_words,cant_lines):
    import statsmodels.api as sm
    alpha = 0.05
    for pair in itertools.combinations(pais, 2):
        start = datetime.datetime.now()
        pvalores = {}
        p1 = pair[0]
        p2 = pair[1]
        words_pvalues = []
        #agarro el archivo y me fijo las primeras x lineas y de eso agarro los pvalores y los imprimo si superan el umbral
        filename = 'tweetsFinal/listas/'+p1 + '_' + p2
        with open(filename) as fi:
            for i in range(cant_lines):
                line = fi.readline()
                w = line.split('\t')[0]
                #words_pvalues.append(w)
        #for w in words_pvalues:
                n1 = (cant_words[p1])
                n2 = (cant_words[p2])
                X1 = 0.0 if not(words[p1].has_key(w)) else words[p1][w]
                X2 = 0.0 if not(words[p2].has_key(w)) else words[p2][w]
                z_score, p_value = sm.stats.proportions_ztest([X1, X2], [n1, n2])
                if not math.isnan(p_value) : # son nan si X1 y/o X2 son 0
                    #print (alpha* i / cant_lines)
                    #if p_value < (alpha* i / cant_lines):
                    pvalores[w] = p_value
                    
        save_list_words(pvalores,words,cant_words,p1,p2)
        end = datetime.datetime.now()
        print p1,p2, end - start


litoral  = ['santacruz', 'tierradelfuego', 'chubut', 'rionegro',"neuquen", 'lapampa','buenosaires','santafe','entrerios']
cuyo = ['mendoza']
central= ['sanluis','cordoba']
guaranitica = ['corrientes', 'misiones', 'chaco', 'formosa']
noroeste = ['santiago', 'larioja', 'catamarca','sanjuan', 'jujuy', 'salta', 'tucuman']
regiones = {}
#litoral_dict = cuyo_dict = guaranitica_dict = noreoeste_dict = central_dict = {}
for prov in litoral:
    regiones[prov] = 'litoral'
for prov in cuyo:
    regiones[prov] = 'cuyo'
for prov in guaranitica:
    regiones[prov] = 'guaranitica'
for prov in noroeste:
    regiones[prov] = 'noroeste'
for prov in central:
    regiones[prov] = 'central'

def region (prov):
    return regiones[prov]



def save_regions(words,cant_words):
    words_region = {}
    cant_words_region = {}
    for prov in words:
        la_region = region(prov)
        if la_region not in words_region:
            words_region[la_region] = {}
            cant_words_region[la_region] = cant_words[prov]
        else:
            cant_words_region[la_region] += cant_words[prov]
        for w in words[prov]:
            if w in words_region[la_region]:
                words_region[la_region][w] += words[prov][w]
            else:
                words_region[la_region][w] = words[prov][w]

    with open(path + 'regiones.json', 'w') as fp:
        json.dump(words_region, fp)
    with open(path + 'cant_words_region.json', 'w') as fp:
        json.dump(cant_words_region, fp)
    return words_region,cant_words_region

 

if __name__ == "__main__":

    start_todo = datetime.datetime.now()
    save_dicts(argentina)
    words,cant_words = load_dicts(argentina)
    words_region,cant_words_region=save_regions(words,cant_words)
    #test_par_provincias(words,cant_words,argentina)
    test_par_provincias(words_region,cant_words_region,list(set(regiones.values())))
    end_todo = datetime.datetime.now()
    print end_todo - start_todo
    