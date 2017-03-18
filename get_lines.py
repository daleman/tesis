# coding: utf-8

import json
import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame, Series
import itertools


regiones = ['litoral', 'central', 'cuyo', 'noroeste', 'guaranitica']

for pair in itertools.combinations(regiones, 2):
    p1 = pair[0]
    p2 = pair[1]
    print p1,p2
    df = pd.read_csv('/home/dami/tesis/train/listas/'+p1 + '_'+p2+'.csv',sep=",",delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    df = df[df['Pvalue'] <= 0.05]
    #df['fnorm1'] = df.Age.apply(lambda x: x if not pd.isnull(x) else 'Is Null value')
    mini = df[df > 0].fnorm1.min() 
    print df[df > 0].fnorm1.min(), 'minimo'
    df.fnorm1.replace(0, mini, inplace=True)
    mini = df[df > 0].fnorm2.min() 
    print df[df > 0].fnorm2.min(), 'minimo'
    df.fnorm2.replace(0, mini, inplace=True)
    df['div1'] = df.fnorm1 / df.fnorm2
    df['div2'] = df.fnorm2 / df.fnorm1
    df['maxdif'] = df[['div2','div1']].apply(max, axis=1)
    
    df = df.sort_values('maxdif',ascending = False)
    df = df.drop(['div1','div2'], axis=1)
    print str(p1),str(p2)
    df.rename(columns={'cant P1':'cant '+ p1,'cant P2': 'cant ' + p2 ,'Total P1': 'Total '+ p1,'Total P2': 'Total '+ p2,'Total P1 + P2': 'Total '+ p1 + ' ' + p2,'fnorm1': 'fnorm ' + p1 ,'fnorm2':'fnorm ' + p2}, inplace=True)
    df.to_csv('train/regiones/' + p1 + '_'+p2 + '.csv', encoding='utf-8',quotechar='|', quoting=csv.QUOTE_MINIMAL)