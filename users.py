
# coding: utf-8

import tweepy
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import unicodedata
import math
from apps import *
import datetime
import sys
import pickle
from nltk.tokenize import word_tokenize
reload(sys)
sys.setdefaultencoding('utf-8')

from jujuy_followers import *
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


ids= {}
loc = {}
#word_tokenizer=nltk.data.load('tokenizers/punkt/spanish.pickle')
def autenticar(n_app):

    n_app = n_app % 259
    app = apps[n_app]
    consumer_key = app['consumer_key']
    consumer_secret = app['consumer_secret']
    access_token = app['access_token']
    access_token_secret = app['access_token_secret']
    

    auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)

    auth.set_access_token(access_token, access_token_secret)

    # Creation of the actual interface, using authentication
    api = tweepy.API(auth)

    #Error handling
    if (not api):
        print ("Problem Connecting to API")
    else:
        print "Autenticado " + str(n_app)

    #print api.rate_limit_status()
    return api


def autenticar_app(n_app):

    n_app = n_app % 255
    app = apps[n_app]
    consumer_key = app['consumer_key']
    consumer_secret = app['consumer_secret']
    access_token = app['access_token']
    access_token_secret = app['access_token_secret']

    #Switching to application authentication
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

    #Setting up new api wrapper, using authentication only
    api = tweepy.API(auth) #wait_on_rate_limit=True
     
    #Error handling
    if (not api):
        print ("Problem Connecting to API")
    else:
        print "Autenticado App" + str(n_app)
    return api



def buscar_tweets(prov,api,n_app,printi,cant_tweets):
    
    tweet_count = 0
    cant_tweets = cant_tweets
    coords = provincias[prov]['coords']
    
    f_tweets = open(prov+'_tweets.json','a')
    f_users = open(prov+'_users.json','a')
    usr_prov = 0
    cant_por_coord = 40000
    
    while (usr_prov < cant_tweets):
        for coord in coords:
            if usr_prov >= cant_tweets:
                #print 'break2'
                break

            ic = 0
            #print str(coords.index(coord)) +  '/' + str(len(coords))
            prev = 0
            
            #print 'coord, tweet' ,coord, tweet_count
            #print "Intento " + str(tweet_count)
            act = 0 
            try:
                for tweet in tweepy.Cursor(api.search, count=100,lang="es",geocode=(coord + ',20mi')).items():
                    #print(tweet.id)
                    tweet_count += 1
                    ic += 1
                    if tweet_count % printi == 0:
                        print '\t' , tweet_count, ic, usr_prov, prev
                        if prev and usr_prov - prev < 2:
                            break
                        prev = usr_prov

                    

                    if tweet.user.location!="":  
                        location=unicodedata.normalize('NFKD',tweet.user.location).encode('ASCII', 'ignore').lower().replace('-',' ').replace(';',' ').replace(',',' ').replace('|',' ').replace('?',' ').replace('¿',' ').replace("\ ",' ').replace('/',' ')
                        location = word_tokenize(location)
                        #print location
                        words = provincias[prov]['words']
                        matches=[x for x in location if x in words]
                        if len(matches)>0 and tweet.user.id not in ids:
                            usr_prov += 1
                            
                            f_users.write(json.dumps(tweet._json['user']))
                            f_users.write("\n")
                            f_tweets.write(json.dumps(tweet._json))
                            f_tweets.write("\n")
                            ids[tweet.user.id] = 1
                            location = tweet.user.location
                            loc[location] = 1 if not loc.has_key(location) else loc[location] +1
                            if usr_prov >= cant_tweets:
                                #print 'break2'
                                break
                            
                    if ic >= cant_por_coord:
                        #print 'break1'
                        break
                            
            except tweepy.TweepError,e:
                n_app += 1
                #print "Error " + str(e)
                api = autenticar_app(n_app)
                continue
            except Exception, e:
                #print "Error " + str(e)
                continue

    f_tweets.close()
    f_users.close()
    return n_app

def plot(canti):
    plt.title("Histograma de lugares")
    plt.xlabel("Lugares")
    plt.ylabel("Frecuencia")

    index = np.arange(len(loc.keys()))
    bar_width = 0.35


    cant = canti
    valores = sorted(loc.values(),reverse=True)
    claves = sorted(loc, key=loc.get,reverse=True)

    opacity = 0.4
    plt.xticks(index + bar_width, claves[:cant], size=6, rotation="vertical")
    plt.bar(range(cant),valores[:cant],alpha=opacity,color='b',)
    plt.tight_layout()
    plt.show()

    
def usuarios_prov(mod_print,tot_tweets,n_app):
    api = autenticar(n_app)
    for prov in provincias.keys():
        start = datetime.datetime.now()
        #print provincias[prov]['name']
        n_app = buscar_tweets(prov,api,n_app,mod_print,tot_tweets)
        end = datetime.datetime.now()
        diff = (end - start)
        print provincias[prov]['name'] , diff

    print str(tot_tweets * len(provincias.keys())), len(ids)
    with open('location.json','w') as a_file:
        a_file.write(json.dumps(loc))
    return n_app

def listDict_toDataFrame(locs):

    data=[] 
    for loc in locs:
        li = []        
        for prov in provincias:
            li.append(loc[prov])
        data.append(li)
    
    df=pd.DataFrame(data=data,columns=provincias.keys())

    return df

def followers(prov, n_app, f_out):
    api = autenticar_app(n_app)
    with open(f_out,'a') as f:
        f.write( prov + "={" )
        f.write('\n')
    locs = []
    screen_names = []
    with open('./ult_json/' + prov + '_users.json', "r") as ins:
        for line in ins:
            d = json.loads(line)
            sc = d["screen_name"]
            screen_names.append(sc)
    
    ind = -1
    while ind < (len(screen_names)):
        ind +=1
        sc = screen_names[ind]
        loc_d = {}
        for pr in provincias:
            loc_d[pr] = 0
        folls = 0.0
        try:
            print ind,sc
            for user in tweepy.Cursor(api.followers,count=200, screen_name=sc).items():
                #print '\t',user.screen_name, user.location
                
                if user.location!="":  
                    location=unicodedata.normalize('NFKD',user.location).encode('ASCII', 'ignore').lower().replace('-',' ').replace(';',' ').replace(',',' ').replace('|',' ').replace('?',' ').replace('¿',' ').replace("\ ",' ').replace('/',' ')
                    location = word_tokenize(location)
                    #print location
                    for pr in provincias:
                        words = provincias[pr]['words']
                        matches=[x for x in location if x in words]
                        if len(matches)>0:
                            folls += 1
                            loc_d[pr] += 1
            for k in loc_d.keys():
                loc_d[k] =  loc_d[k] / folls
            locs.append(loc_d)
            with open(f_out,'a') as f:
                f.write( "'" +str(sc) + "':" + str(loc_d) +',')
                f.write('\n')
        except tweepy.TweepError,e:
            ind = ind -1
            print ind
            n_app += 1
            #print "Error " + str(e)
            api = autenticar_app(n_app)
            continue
        except Exception, e:
            #print "Error " + str(e)
            continue
    with open(f_out,'a') as f:
        f.write( "}" )
        f.write('\n')
    print 'guardo en archivo ' + prov
    df = listDict_toDataFrame(locs)
    df['class'] = prov
    df.to_pickle(pr + '.pkl')                
    return n_app

    
if __name__ == "__main__":
    # n_app = 0
    # start = datetime.datetime.now()
    
    # #n_app = int(sys.argv[1])
    # #prov = sys.argv[2]
    # #api = autenticar(n_app)
    # #mod_print = 400
    # #tot_tweets = 10000

    # n_app = usuarios_prov(400,10000,n_app)
    # end = datetime.datetime.now()

    # #start = datetime.datetime.now()
    # #print provincias[prov]['name']
    

    # #n_app = buscar_tweets(prov,api,n_app,mod_print,tot_tweets)
    # #end = datetime.datetime.now()
    # diff = (end - start)
    # #print provincias[prov]['name'] , diff


    # print 'Todas las provincias en: ' + str(end -start)

    # ##n_app = int(sys.argv[1])
    # ##pr = sys.argv[2]
    # ##print n_app, pr
    # n_app = followers(pr,n_app, pr + '_followers.json')
    
    # for prov in provincias:
    #     start = datetime.datetime.now()
    #     n_app = followers(prov,n_app, prov + '_followers.json')
    #     end = datetime.datetime.now()
    #     print provincias[prov]['name'] ,str(end -start)
    
    # #plot(20)

    frames = []
    for pr in provincias:
        with open('provs/' + pr + '.pkl') as f:
            df = pd.DataFrame(pickle.load(f))
        #df = pd.read_pickle('provs/' + pr + '.pkl')
        df['class'] = pr
        frames.append(df)
        df.to_pickle(pr + '.pickle')
    result = pd.concat(frames,ignore_index=True,keys=provincias.keys())
    print result.describe()
    y = result['class']
    X = result.drop('class', 1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    result.to_pickle('features.pickle')
    clf = RandomForestClassifier()
    clf.fit(X_train,y_train)
    y_pred = clf.predict(X_test)
    print accuracy_score(y_test, y_pred)
