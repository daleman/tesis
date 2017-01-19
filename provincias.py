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
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#consumer_key ="fshtLxpED9vXbZl5gVkaSowGr"
#consumer_secret = "H2qEQC4wU2a1IkbKpNMlVbac1IV0vWlZMPmoyfyAVZCmZfUuZa"
#access_token = "3377301250-BAi7czgq59etPjYpZWFfJHOHIf048vaxsJ9G9Yo"
#access_token_secret = "mpIeF0mEGjFTwUIUtd9nr20nu8O675zEFZlVPuTt12jcF"


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

def buscar_tweets(api,n_app,place_id,printi,cant_tweets):
	
	tweet_count = 0
	cant_tweets = cant_tweets
	
	ids= {}

	while tweet_count < cant_tweets:
		try:
			print "Intento " + str(tweet_count)
			for tweet in tweepy.Cursor(api.search,q="place:%s" % place_id,count = 100).items():
				#print(tweet.id)
				tweet_count += 1
				if tweet_count % printi == 0:
					print tweet_count
				if tweet.user.location!="":  
					location=unicodedata.normalize('NFKD',tweet.user.location).encode('ASCII', 'ignore').lower().replace('-',' ').replace(';',' ').replace(',',' ').replace('|',' ').replace('?',' ').replace('¿',' ').replace("\ ",' ').replace('/',' ')
					seg = 0
					for prov in provincias.keys():
						words = provincias[prov]['words']
						matches=[x for x in location.split(' ') if x in words]
						if len(matches)>0 and tweet.user.id not in ids:
							files_prov[prov]['users'].write(json.dumps(tweet._json['user']))
							files_prov[prov]['users'].write("\n")
							files_prov[prov]['tweets'].write(json.dumps(tweet._json))
							files_prov[prov]['tweets'].write("\n")
							ids[tweet.user.id] = 1
							seg +=1
						if seg> 1:
							print "lo agrego " + seg + "veces"
					if tweet_count >= cant_tweets:
						break
		except tweepy.TweepError:
			n_app += 1
			api = autenticar_app(n_app)
			continue
		except Exception, e:
			print"Error " + str(e)
			continue
	for f_prov in files_prov.keys():
		files_prov[f_prov]['users'].close()
		files_prov[f_prov]['tweets'].close()
	


	return


if __name__ == "__main__":

	n_app = 10
	api = autenticar(n_app)

	q= "Argentina"
	places = api.geo_search(query=q,granulartity='country')
	place_id = places[0].id
	print "id de " + str(q) + ": " +places[0].id, places[0].full_name #hay varios places Argentina, pero solo el primero es el pais 

	buscar_tweets(api,n_app,place_id,2000,1000000)

	#place_id = 0
	#for prov in provincias.keys():
		#try:
			#print provincias[prov]['name']
			#places = []
			#places = api.geo_search(query=provincias[prov]['name'],granulartity='city')
			#if len(places) != 0:
				#print "tiene " + str(len(places))
				#for place in places:
					#place_id = place.id
					#if  place.country == 'Argentina':
						#print "id de " + str(place.full_name) +' ' +  str(place.country) + ": " + str(place_id)
						#print place.bounding_box.coordinates
			#buscar_tweets(prov,api,n_app,place_id,10000,1000000)
					#else:
					#	print 'no busco porque ' + place.country  + " no es argentina"
			#else:
			#	print prov + " no tiene places"
		#except tweepy.TweepError:
		#	n_app += 1
		#	api = autenticar(n_app)
		#	continue
		#except Exception, e:
		#	print"Error aca " + str(e)
		#	continue

	