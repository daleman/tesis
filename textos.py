# coding: utf-8
import json
from apps import *
import matplotlib.pyplot as plt
import numpy as np
import re
from nltk import word_tokenize
from string import punctuation
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# emoji_pattern = re.compile(
#     u"(\ud83d[\ude00-\ude4f])|"  # emoticons
#     u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
#     u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
#     u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
#     u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
#     "+", flags=re.UNICODE)


def plot(canti,dic):
	plt.title("Frecuencia de Palabras")
	plt.xlabel("Palabras")
	plt.ylabel("Frecuencia")

	index = np.arange(len(dic.keys()))
	bar_width = 0.35


	cant = canti
	valores = sorted(dic.values(),reverse=True)
	claves = sorted(dic, key=dic.get,reverse=True)

	opacity = 0.4
	plt.xticks(index + bar_width, claves[:cant], size=6, rotation="vertical")
	plt.bar(range(cant),valores[:cant],alpha=opacity,color='b',)
	plt.tight_layout()
	plt.show()


def dictionary(words,provincia):
	file_path = 'txt/tweets/' + provi + '_textos.json'
	with open(file_path) as f:
		for line in f:
			content = json.loads(line)
			texto =  content['text']
			texto = ' '.join(word for word in texto.split(' ') if not word.startswith('#'))
			texto = ' '.join(word for word in texto.split(' ') if not word.startswith('@'))
			texto = re.sub(r'http\S+', '', texto)
			m = re.findall('[^\W\d]+', texto, re.UNICODE)
			#import ipdb; ipdb.set_trace()
			#print m
			txt =' '.join(m)
			print txt
			texto =  word_tokenize(txt)
			#print texto
			for w in texto:
				wl = w.lower()
				words[wl] = 1 if not words.has_key(wl) else words[wl] +1
	return words

def save_texts(provincia):
	file_path = provi + '_textos.json'
	file_w =  provi + '_solo_texto.json'
	with open(file_path) as f:
		for line in f:
			content = json.loads(line)
			texto =  content['text']
			with open(file_w,'a') as fi:
				fi.write(texto)
				fi.write('\n')
	return words

def tokenize(text):
    text = re.sub('[\W_]+', ' ', text)
    tokens =  word_tokenize(text)
    return tokens

if __name__ == "__main__":

	words = {}
	non_words = list(punctuation)
	non_words.extend(['¿', '¡','*','!'])
	non_words.extend(map(str,range(10)))
	for provi in provincias:
		words = dictionary(words,provi)
	#provi = 'jujuy'
	#save_texts(provi)

	cant_words = 0.0
	for w in words:
		cant_words += words[w]

	print "la cantidad total de palabras es " + str(cant_words)
	print "palabra,#ocurrencias,Fnorm" 

	for wo in sorted(words, key=words.get, reverse=True):
  		with open('dicc','a') as fi:
			fi.write(wo.encode('utf-8')+ "," +  str(words[wo]) + ","  + str(words[wo] / (cant_words/1000000)) + '\n')
		
  	
  	#plot(100,words)