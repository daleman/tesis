# coding: utf-8
from apps import argentina
import pandas as pd
import json
import numpy as np
import re
from scipy import stats
import matplotlib.pyplot as plt
import datetime


def H(value1,value2):
    x = 0
    if value1 > value2:
        x=1
    elif value1 == value2:
        x=0.5
    return x
 
# Bootstrap test
def bootstraptest (data1,data2,N):
    n = min(len(data1),len(data2))
    p1 = 0
    for i in range(N):
        p1 = p1 + H( data1.sample(n=n,replace=True).mean(),data2.sample(n=n,replace=True).mean() )
    p1 = p1/float(N)
    p2 = (1+2*N*min(p1,1-p1))/float((1+N))
    return p2


def region(palabra):
    return listaProvincias(df2.loc[palabra,'regionTest'])

def sacarCorchetesYComillas(nombre):
    return re.sub("\\[|\\]| |'", "", nombre)

#la region que toma como parametro esta en formato de lista pero es un string, por eso lo parseo
def listaProvincias(region):
    return map(sacarCorchetesYComillas,region.split(','))


def frecuenciaProvincial(palabra,provincia):
    """ Devuelve las frecuencias de la palabra por cada usuario en esa provincia """
    if (palabra not in freqs[provincia].index):
        return pd.Series(np.zeros(len(freqs[provincia].columns)))
    else:
        return freqs[provincia].loc[palabra]

def frecuenciaRegional(palabra,region):
    return pd.Series().append([frecuenciaProvincial(palabra,provincia) for provincia in region])


def restoPais(region):
    """ calcula el conjunto de provincias que no son parte de la region pasada por parametro """
    return [x for x in provincias if x not in region]

#len(frecuenciaRegional('que',['buenosaires','entrerios']))

# calcula la region de la palabra y el resto del pais
# luego obtiene las frecuencias en cada region y realiza el bootrstrap test a partir de esos vectores de frecuencias
def pvalor(palabra,N=100000):
    """calcula el pvalor asociado a que la palabra ocurra mas(o menos) en la region que en el resto del pais"""
    region1 = region(palabra)
    region2 = restoPais(region1)
    freqs1 = (frecuenciaRegional(palabra,region1))
    freqs2 = (frecuenciaRegional(palabra,region2))
    freqs1.fillna(0)
    freqs2.fillna(0)
    return bootstraptest(data1 = freqs1,data2 = freqs2,N=N)

def welch(palabra):
    a = frecuenciaRegional(palabra,region(palabra))
    b = frecuenciaRegional(palabra,restoPais(region(palabra)))
    pvalue = stats.ttest_ind(a, b, equal_var = False)[1]
    #print(palabra,pvalue)
    return pvalue

def wilcoxon(palabra):
    a = frecuenciaRegional(palabra,region(palabra))
    b = frecuenciaRegional(palabra,restoPais(region(palabra)))
    minl = min(len(a),len(b))
    a=a.sample(n=minl,replace=True)
    b=b.sample(n=minl,replace=True)
    pvalue = stats.wilcoxon(a, b)[1]
    print(palabra,pvalue)
    return pvalue

def mannw(palabra):
    a = frecuenciaRegional(palabra,region(palabra))
    b = frecuenciaRegional(palabra,restoPais(region(palabra)))
    minl = min(len(a),len(b))
    a=a.sample(n=minl,replace=True)
    b=b.sample(n=minl,replace=True)
    pvalue = stats.mannwhitneyu(a, b)[1]
    #print(palabra,pvalue)
    return pvalue


path = '../Desktop/datosTesis/train/train_'
def load_dict(provincia):
    dicc_usuarios = {}
    print provincia
    with open(path + provincia + '_users_dict.json') as fi:
        dicc_usuarios = json.load(fi)
    return  dicc_usuarios



""" Este script toma los diccionarios hechos por la funcion dictionary de textos.py y
 genera .csv que tienen la cantidad de ocurrencias de las palabras por cada usuario.
"""

# for p in argentina:
#     dicc_usuarios = load_dict(p)
#     df = pd.DataFrame.from_dict(dicc_usuarios,orient='index')
#     df = df.drop('user_id', 1)
#     df.fillna(0,inplace=True)
#     ser = df.sum(axis=0)
#     df = (df / ser)*1000000
#     df.to_csv('./dataUsuarios/{0}.csv'.format(p),encoding='utf-8')

# ivalues tiene el csv con las regiones de cada palabra. Estas regiones estan en formato de lista pero como un string
# por lo tanto se parsea
ivalues = 'notebooks/ivalue_entropia_personas_palabras.csv'
df2 = pd.DataFrame.from_csv(ivalues,header=0,encoding='utf-8')

# filtro solamente las palabras que estan en ivalues (las que tienen mas de 40 apariciones y dichas por mas de 6 usuarios)
# for p in argentina:
#     df = pd.read_csv('./dataUsuarios/{0}.csv'.format(p),encoding= 'utf-8',index_col=0)
#     df = df[ df.index.isin(df2.index)]
#     df.to_csv('./dataUsuarios/filtrado/{0}.csv'.format(p),encoding='utf-8')
#     print(p,str(df.shape))

# listado de todas las provincias de argentina
provincias = ['jujuy',  'catamarca',  'sanjuan',  'salta',  'rionegro',  'lapampa',  'chaco',
               'mendoza',  'buenosaires',  'entrerios',  'chubut',  'santacruz',  'neuquen',
               'misiones',  'corrientes',  'formosa',  'santafe',  'santiago',  'cordoba',  'larioja',  'tierradelfuego',  'tucuman',  'sanluis']


# el path donde se encuentran los .csv con la cantidad de ocurrencias de cada palabra por cada usuario.
# hay un csv por cada provincia, con el nombre [nombreProvincia].csv
path = '/home/dami/tesis/dataUsuarios/filtrado/'


# leo todos los .csv de cada provincia y creo variables con los dataframes de cada provincia con su nombre respectivo.
# ej. la variable buenosaires va a tener el dataframe de buenos aires

freqs = {}
for p in provincias:
    start = datetime.datetime.now()
    freqs[p] = pd.DataFrame.from_csv(path = path+p+'.csv',encoding='utf-8') # probar con encoding='utf-8'
    end = datetime.datetime.now()
    print(p,str(end-start))
# print(pvalor('abrigos',2000))
# print(pvalor('angá',2000))
start = datetime.datetime.now()
df3 = df2[:10]
df3['pvalorWelch'] = df3.apply(lambda x: welch(x.name),axis=1)
df2.to_csv('./testEstadisticos/welchTest.csv',encoding='utf-8')
end = datetime.datetime.now()
print(p,str(end-start))
# start = datetime.datetime.now()
# df6 = df2[:30000]
# df6['pvalorBootstrap'] = df6.apply(lambda x: pvalor(x.name,2000),axis=1)
# df6.to_csv('./testEstadisticos/bootstraptest.csv',encoding='utf-8')
# end = datetime.datetime.now()
# print(p,str(end-start))