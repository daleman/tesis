# coding: utf-8

import tweepy
from apps import *

import re
import json
import nltk
from nltk.tokenize import word_tokenize
import datetime
import unicodedata
import string
import sys
import argparse

def tokenize(text):
    text = re.sub('@[\w]*', '', text)
    text = re.sub('#[\w]*', '', text)
    text = re.sub(r'http\S+', '', text)
    text = re.findall('[^\W\d]+', text, re.UNICODE)
    text =' '.join(text)
    tokens =  word_tokenize(text)
    return tokens

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


def save_tweet(tweet,str_file_tweet):
     with open(str_file_tweet,'a') as a_file:
        json.dump(tweet._json, a_file)
        a_file.write('\n')    

def save_text(tweet,str_file_text):
    with open(str_file_text,'a') as a_file:
        a_file.write(tweet.text.encode('utf-8') + '\n')

def save_tokens(tokens,str_file_text):
    with open(str_file_text,'a') as a_file:
        json.dump(tokens, a_file)
        a_file.write('\n')

def save_dat(i,tot,total,cant_tot_tweets,str_file_dat):
    with open(str_file_dat,'a') as a_file:
        a_file.write(str(i) + '\t' + str(tot) + '\t' + str(total) + '\t' +  str(cant_tot_tweets))
        a_file.write('\n') 

def save_tiempos(prov,start,printi,str_file_tiempos):
    end = datetime.datetime.now()
    print prov, end - start
    with open(str_file_tiempos,'a') as fil:
        fil.write(str(printi) + ' ' + prov + ' ' + str(end-start) + '\n')


def tweets_prov(app,api,file_users,cant_tweets_max_usuario,cant_words_prov ,num_usr,cant_max_tweets):
    total_words = 0         # cantidad total de palabras
    cant_tot_tweets = 0
    start = datetime.datetime.now()
    word_tokenizer=nltk.data.load('tokenizers/punkt/spanish.pickle')
    i = 0
    #los_dias = 'pares' if pares else 'impares'

    print prov

    with open(file_users) as f:
        for line in f:
            #if i < num_usr:
            #    i+=1
            #    continue            
            d = json.loads(line)
            try:
                elid = d['id']
                words_user_tot = 0
                cant_tweets = 0
                
                for t in tweepy.Cursor(api.user_timeline, id=elid,count = 200, include_rts = False ).items():
                    #dia = t.created_at.weekday()
                    #if dia in dias:
                    cant_tweets +=1
                    #texto = tokenize(t.text)
                    save_tweet(t,'tweetsFinal2/' + prov  + '_tweets.json')
                    # Dejo la tokenizacion como post procesamiento
                    #save_text(t,'tweetsFinal2/' + los_dias + '/' + prov  + '_text.txt')
                    #save_tokens(texto,'tweetsFinal2/' + los_dias + '/' + prov  + '_tokens.txt')
                    #l = len(texto)
                    #words_user_tot += l
                    #if cant_tweets == cant_tweets_max_usuario:
                    #    break 
                #total_words += words_user_tot
                cant_tot_tweets += cant_tweets
                num_usr+=1
                save_dat(num_usr,words_user_tot,total_words,cant_tot_tweets,'tweetsFinal2/' +  prov  + '.dat')
                
                #if total_words > cant_words_prov:
                #if cant_tot_tweets > cant_max_tweets:
                #    save_tiempos(prov,start,cant_words_prov,'tweetsFinal2/' + 'tiempos.dat')
                #    break
            except Exception, e:   
                app += 1
                print "Error " + str(e)
                api = autenticar_app(app)
                continue

    save_tiempos(prov,start,cant_words_prov,'tweetsFinal2/' + 'tiempos.dat')
    return num_usr
     

if __name__ == "__main__":

    
    parser = argparse.ArgumentParser()
    parser.add_argument("app", help="el numero de aplicacion con que empieza la busqueda",
                        type=int)
    parser.add_argument("provincia", help="la provincia donde se van a buscar los usuarios",
                        type=str)
 

    args = parser.parse_args()
    n_app = args.app
    prov = args.provincia

    api = autenticar_app(app)

    cant_tweets_max_usuario = 600
    cant_words_prov = 6000000
    num_usr = 0
    n = tweets_prov(app,api,'ult_json/' + prov + '_users.json',cant_tweets_max_usuario,cant_words_prov,num_usr,500000)
  