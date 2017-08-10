# coding: utf-8
import pandas as pd
import csv
import json
import pprint

argentina = ['jujuy', 'catamarca', 'sanjuan', 'salta', 'rionegro',
 'lapampa', 'chaco', 'mendoza', 'buenosaires', 'entrerios',
 'chubut', 'santacruz', 'neuquen', 'misiones', 'corrientes', 'formosa',
 'santafe', 'santiago', 'cordoba', 'larioja', 'tierradelfuego', 'tucuman', 'sanluis']

coords,locations = {},{}
path = 'tweets/'
for p in argentina:
    locations[p] = {}
uids = set()
    
for p in argentina:
    with open('{0}{1}_tweets.json'.format(path,p)) as f:
        df = pd.read_csv('train/train_{0}.csv'.format(p),encoding='utf-8', delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        usuarios = (df.user_id.unique())        
        for line in f:
            tweet = json.loads(line)
            uid = tweet['user']['id']
            # coord = tweet['coordinates']
            # pp = pprint.PrettyPrinter(indent=4)
            location = tweet['user']['location'].lower() 
            if uid in usuarios and uid not in uids:
                if location not in locations[p]:
                    locations[p][location] = 1
                else:
                    locations[p][location] += 1
                uids.add(uid)
                
with open('locations.json', 'w') as fp:
    json.dump(locations, fp)
