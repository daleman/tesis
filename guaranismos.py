# coding: utf-8
import pandas as pd
import csv
import os
pd.set_option('display.max_colwidth', 140)


# Regiones dialectales definidas por Vidal de Batini
litoral = ['santacruz', 'tierradelfuego', 'chubut', 'rionegro',
           "neuquen", 'lapampa', 'buenosaires', 'santafe', 'entrerios']
cuyo = ['mendoza']
central = ['sanluis', 'cordoba']
guaranitica = ['corrientes', 'misiones', 'chaco', 'formosa']
noroeste = ['santiago', 'larioja', 'catamarca',
            'sanjuan', 'jujuy', 'salta', 'tucuman']

cols = ['tweet_created_at','created_at','user_id','text']
parse_dates = ['tweet_created_at', 'created_at']
frames = []
for p in guaranitica:
    df = pd.read_csv('csv/train_{0}.csv'.format(p),usecols=cols,encoding='utf-8',delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL, parse_dates=parse_dates)
    frames.append(df)
guarani = pd.concat(frames,keys = guaranitica,names=['provincias','nro'])

def tableWithPattern(df,pattern):
    return df[df.text.str.contains(pattern,case=False)]

# creo la carpeta resultados si no existe
if not os.path.exists('latex/src/resultados'):
    os.makedirs('latex/src/resultados')

# pat = r'\bmitaí|\bmitaii|\bmitai|\bmitaises|\bmitaices|\bmitais'
pat = r'\bMITA(Í|I)+([A-Z])*\b'
print tableWithPattern(guarani,pat).groupby(level=0).text.count()

tableWithPattern(guarani,pat).to_latex('latex/src/resultados/mitai.tex',encoding='utf-8')

# pat = 'angau|engauu|engau'
pat = r'\b(A|E)NGA(U|Ú)+\b'
print tableWithPattern(guarani,pat).groupby(level=0).text.count()
tableWithPattern(guarani,pat).to_latex('latex/src/resultados/angau.tex',encoding='utf-8')


# pat = 'anga|angaa|angacito'
pat = r'\bANG(A|Á)+(CITO)?\b'
print tableWithPattern(guarani,pat).groupby(level=0).text.count()
tableWithPattern(guarani,pat).to_latex('latex/src/resultados/anga.tex',encoding='utf-8')
