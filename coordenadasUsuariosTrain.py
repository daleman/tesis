# coding: utf-8
import pandas as pd
import csv
import json

argentina = ['jujuy', 'catamarca', 'sanjuan', 'salta', 'rionegro',
 'lapampa', 'chaco', 'mendoza', 'buenosaires', 'entrerios',
 'chubut', 'santacruz', 'neuquen', 'misiones', 'corrientes', 'formosa',
 'santafe', 'santiago', 'cordoba', 'larioja', 'tierradelfuego', 'tucuman', 'sanluis']

coords = {}
path = '../tweetsFinal/pares/'
for p in argentina:
    with open('{0}{1}_tweets.json'.format(path,p)) as f:
        df = pd.read_csv('../train/train_{0}.csv'.format(p),encoding='utf-8', delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        usuarios = (df.user_id.unique())        
        for line in f:
            tweet = json.loads(line)
            uid = tweet['user']['id']
            coord = tweet['coordinates']
            if coord and uid in usuarios:
                coordenadas = str(coord['coordinates'])[1:-1]
                if coordenadas not in coords:
                    coords[coordenadas] = 1
                else:
                    coords[coordenadas] +=1

with open('latex/src/resultados/coords.txt','a') as f: 
    for c,w in coords.iteritems():
        f.write('{location: new google.maps.LatLng(' + c.split(',')[1][1:] +','+ c.split(',')[0] + '), weight: '+ str(w)+'},')

print(str(len(coords)))