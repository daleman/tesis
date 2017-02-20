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

path = 'tweetsFinal/impares/' 


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
    file_path = path + provincia + '_tokens.txt'
    with open(file_path) as f:
        for line in f:
            #content = json.loads(line)
            #texto =  content['text']
            #texto = tokenize(texto)
            texto = json.loads(line)
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
    return n /(cant_words[provincia]/1000000)

def mean(provincia,word):
    return words[provincia][word]/cant_words[provincia]

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
    texto = re.sub('@[\w]*', '', texto)
    texto = re.sub('#[\w]*', '', texto)
    texto = re.sub(r'http\S+', '', texto)
    texto = re.findall('[^\W\d]+', texto, re.UNICODE)
    texto =' '.join(texto)
    tokens =  word_tokenize(texto)
    return tokens

def ztest(x1,x2,n1,n2):
    from numpy import sqrt
    p1 = x1/n1
    p2 = x2/n2
    p = (x1 + x2) / (n1 + n2)
    den = sqrt(p*(1.0-p)*((1/n1)+(1/n2)))
    z = (p1-p2) / den 
    return z 

def pvalor(z):
    import scipy.stats as st
    nz = z 
    if z > 0:
        nz = -z
    return 2*st.norm.cdf(nz)

def save_dicts():
    words = {}
    cant_words = {}
    for prov in provincias:
        cant_words[prov] = 0
    for prov in provincias:
        start = datetime.datetime.now()
        #words[prov],cant_words[prov] = dictionary(prov)
        dicc = dictionary(prov)
        n_dicc = remove_words(dicc,1)
        words[prov] = n_dicc
        cant_words[prov] = cant_palabras(n_dicc)
        end = datetime.datetime.now()
        with open(path + prov + '_dict.json', 'w') as fp:
            json.dump(words[prov], fp)
        print prov,cant_words[prov], end - start

def load_dicts():    
    words = {}
    cant_words = {}
    for prov in provincias:
        cant_words[prov] = 0
    for prov in provincias:
        print prov
        with open(path+prov+'_dict.json') as fi:
            words[prov] = json.load(fi)
        for w in words[prov]:
            cant_words[prov] += words[prov][w]
    return words,cant_words

def save_list_words(pvalores,words,cant_words,p1,p2):
    import csv
    
    for w in sorted(pvalores,key=pvalores.get):
        with open('tweetsFinal/listas/corcsv/' + str(p1) + '_' + str(p2) + '.csv','a') as fi:
            spamwriter = csv.writer(fi, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            cant_p1 = str(0.0) if not(words[p1].has_key(w)) else str(words[p1][w])
            cant_p2 = str(0.0) if not(words[p2].has_key(w)) else str(words[p2][w])
            fnorm1 = str(fnorm(p1,w,words,cant_words))
            fnorm2 = str(fnorm(p2,w,words,cant_words)) 
            #fi.write(w.encode('utf-8')+ "\t" + cant_p1  + '\t' + cant_p2 + '\t' +  str(pvalores[w]) + '\t' + fnorm1 + '\t' + fnorm2 + '\n')
            
            spamwriter.writerow((w.encode('utf-8'),cant_p1 ,cant_p2 ,str(pvalores[w]) ,fnorm1 ,fnorm2))
          

def test_par_provincias(words,cant_words):
    pvalores = {}
    for pair in itertools.combinations(provincias, 2):
        start = datetime.datetime.now()
        p1 = pair[0]
        p2 = pair[1]
        for w in set(words[p1].keys()+words[p2].keys()):
            n1 = float(cant_words[p1])
            n2 = float(cant_words[p2])
            X1 = 0.0 if not(words[p1].has_key(w)) else words[p1][w]
            X2 = 0.0 if not(words[p2].has_key(w)) else words[p2][w]
            z = ztest(X1,X2,n1,n2)
            pv = pvalor(z)
            pvalores[w] = pv
        save_list_words(pvalores,words,cant_words,p1,p2)
        pvalores = {}
        end = datetime.datetime.now()
        print p1,p2, end - start

def test_par_provincias_bonfarroni(words,cant_words,cant_lines):
   
    
    for pair in itertools.combinations(provincias, 2):
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
                first_word = line.split('\t')[0]
                words_pvalues.append(first_word)
        for w in words_pvalues:
            n1 = float(cant_words[p1])
            n2 = float(cant_words[p2])
            X1 = 0.0 if not(words[p1].has_key(w)) else words[p1][w]
            X2 = 0.0 if not(words[p2].has_key(w)) else words[p2][w]
            z = ztest(X1,X2,n1,n2)
            pv = pvalor(z)
            if not math.isnan(pv) :
                pvalores[w] = pv
        save_list_words(pvalores,words,cant_words,p1,p2)
        end = datetime.datetime.now()
        print p1,p2, end - start



if __name__ == "__main__":

    start_todo = datetime.datetime.now()
    #save_dicts()
    words,cant_words = load_dicts()
    test_par_provincias_bonfarroni(words,cant_words,300)
    end_todo = datetime.datetime.now()
    print end_todo - start_todo
    