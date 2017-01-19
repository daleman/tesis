# coding: utf-8
import json
from apps import *
import matplotlib.pyplot as plt
import numpy as np

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
	file_path = provi + '_textos.json'
	with open(file_path) as f:
		for line in f:
			content = json.loads(line)
			texto =  content['text']
			for w in texto.split():
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


if __name__ == "__main__":

	words = {}

	#for provi in provincias:
		#words = dictionary(words,provi)
	provi = 'jujuy'
	save_texts(provi)	
	#for wo in sorted(words, key=words.get, reverse=True):
  	#	print wo.encode('utf-8'), words[wo]

  	#plot(100,words)