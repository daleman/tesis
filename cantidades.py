# coding: utf-8
from apps import argentina
import pandas as pd
import csv
import json
dicc = {}
lexico = set()

path = 'test/test_'
for prov in argentina:
    df = pd.read_csv(path +'{}.csv'.format(prov),encoding='utf-8', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    cantUsuarios = len(df.user_id.unique()) 
    cantTweets = df.shape[0]
    dicc[prov] = {'cantUsuarios':cantUsuarios,'cantTweets':cantTweets}
    
    with open(path + '{}_dict.json'.format(prov)) as fi:
        prov_dict = json.load(fi)
        cantPalabras = len(prov_dict.keys())
        cantTotal = sum(prov_dict.values())
        lexico.update(prov_dict.keys())
    dicc[prov]['cantPalabras'] = cantPalabras
    dicc[prov]['cantTotal'] = cantTotal
df1 = pd.DataFrame.from_dict(dicc,orient='index')
df1.to_csv('{}cantidadesDataset.csv'.format(path))
print 'La cantidad de palabras distintas recolectadas sobre la Argentina es: ' + str(len(lexico))