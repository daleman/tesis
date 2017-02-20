import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pylab
from pylab import *
from nltk.corpus import stopwords

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def plot(claves,valores,claves2,valores2):
	f = plt.figure(1)
	plt.title("Frecuencia de Palabras Con Stop Words")
	plt.xlabel("Palabras")
	plt.ylabel("Frecuencia")
	pos = np.arange(len(claves))
	width = 1.0     # gives histogram aspect to the bar diagram
	ax = plt.axes()
	ax.set_xticks(pos + (width / 2))
	ax.set_xticklabels(claves, rotation="vertical")
	plt.bar(pos, valores, width, color='r')
	
	g = plt.figure(2)
	plt.title("Frecuencia de Palabras Sin Stop Words")
	plt.xlabel("Palabras")
	plt.ylabel("Frecuencia")
	pos = np.arange(len(claves))
	width = 1.0     # gives histogram aspect to the bar diagram
	ax2 = plt.axes()
	ax2.set_xticks(pos + (width / 2))
	ax2.set_xticklabels(claves2, rotation="vertical")
	plt.bar(pos, valores2, width, color='b')

	f.show()
	g.show()
	raw_input()



def read_dicc(file_path,tot):
	i = 0
	total = 0
	claves = []
	valores = []
	tot = 100
	with open(file_path) as f:
		for line in f:
			l = line.split()
			word = l[0]
			frequency = int(l[1])
			if word not in stopwords.words('spanish'):
				claves.append(word)
				valores.append(float(frequency))
				i+=1
			else:
				print word
			if i == tot:
				break
			total += frequency
		print total
	return claves,valores


def read_dicc_stop(file_path,tot):
	i = 0
	total = 0
	claves = []
	valores = []
	tot = 100
	with open(file_path) as f:
		for line in f:
			l = line.split()
			word = l[0]
			frequency = int(l[1])
			claves.append(word)
			valores.append(float(frequency))
			i+=1
			if i == tot:
				break
			total += frequency
		print total
	return claves,valores

def save_texts(file_path)
	i = 0
	total = 0
	claves = []
	valores = []
	tot = 100
	with open(file_path) as f:
		for line in f:
			l = line.split()
			word = l[0]
			frequency = int(l[1])
			claves.append(word)
			valores.append(float(frequency))
			i+=1
			if i == tot:
				break
			total += frequency
		print total
	return claves,valores
	


if __name__ == "__main__":

	claves,valores = read_dicc_stop('dicc2',100)
	claves2,valores2 = read_dicc('dicc2',100)
	#plot(claves,valores,claves2,valores2)

