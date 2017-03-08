# coding: utf-8


import os
from pygeocoder import Geocoder

from apps import *
import nltk
import string
from nltk.tokenize import word_tokenize
import unicodedata


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def clean_words(loc):
    bad_words = ['de','del','y', 'el', 'la', 'los', 'las']
    res = list(set(loc))
    res = [x for x in res if x not in bad_words]
    return res
def words_from_location(location):
    words =unicodedata.normalize('NFKD',location.decode('utf-8')).encode('ASCII', 'ignore').lower().replace('-',' ').replace(';',' ').replace(',',' ').replace('|',' ').replace('?',' ').replace('¿',' ').replace("\ ",' ').replace('/',' ')
    words = word_tokenize(words)
    words = clean_words(words)
    return words
import json
import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame, Series
import pprint

if __name__ == "__main__":

    pais_str = sys.argv[1] 
    df = pd.read_csv('/home/dami/Downloads/'  + pais_str +'.csv',sep=",")
    pais = {}
    for index, row in df.iterrows():
        dept = row['Departamento']
        city = row['Ciudad']
        try:
            result = Geocoder.geocode(city+',' + pais_str)
            coord = str(result.coordinates[0]) + ',' + str(result.coordinates[1])
            if not pais.has_key(dept):
                city_dept = city + ' ' + dept
                location = words_from_location(city_dept)
                pais[dept] = {"name":dept,"coords":[coord],"words":location} 
                 
            else:
                pais[dept]['coords'].append(coord)
                location = words_from_location(city)
                pais[dept]['words']+= location
                
        except Exception, e:
            print "Error " + str(e) 
            continue
            #print row['Ciudad'], row['Departamento']
    pprint.pprint(pais)

    with open(pais_str + '.json', 'w') as fp:
        json.dump(pais, fp)