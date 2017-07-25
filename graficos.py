# coding: utf-8

from apps import argentina
import csv
from nltk.tokenize import TweetTokenizer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def set_style():
    plt.style.use(['seaborn-paper', 'seaborn-white'])
    plt.rc("font", family="Times New Roman")


def cantPalabrasPromedio(df):
    cantPalMedia = df.groupby('user_id').cantPalabras.mean()
    ax = sns.distplot(a=cantPalMedia,hist=True,kde=False,bins=100)
    ax.set_xlabel('Cantidad de palabras promedio por usuario')
    ax.get_figure().savefig("{0}cantPalabrasPromedio{1}{2}.pdf".format(relativePathImages,path,pathFiltro),dpi=300)
    plt.close(ax.get_figure())

def cantPalabrasUsuario(df):
    ax = sns.distplot(df.groupby('user_id').cantPalabras.sum(),hist=True,kde=False)
    ax.set_xlabel('Cantidad de palabras por usuario')
    ax.get_figure().savefig("{0}cantPalabrasUsuario{1}{2}.pdf".format(relativePathImages,path,pathFiltro),dpi=300)
    plt.close(ax.get_figure())

def cantTweetsUsuario(df):
    ax = sns.distplot(arg.groupby('user_id').cantPalabras.count(),hist=True,kde=False)
    ax.set_xlabel(u'Cantidad de tweets por usuario')
    ax.get_figure().savefig("{0}cantTweetsUsuario{1}{2}.pdf".format(relativePathImages,path,pathFiltro),dpi=300)
    plt.close(ax.get_figure())

def histTweets1(df):
    ax = df.tweet_created_at.groupby(level=[0]).get_group('lapampa').hist(bins=100,alpha=0.5,color='red',label = 'La Pampa',stacked=True)
    df.tweet_created_at.groupby(level=[0]).get_group('buenosaires').hist(bins=100,ax=ax,color='green',alpha=0.5,label='Buenos Aires',stacked=True)
    ax.legend()
    ax.get_figure().savefig("{0}histTweetsProvincia1{1}{2}.pdf".format(relativePathImages,path,pathFiltro),dpi=300)
    plt.close(ax.get_figure())

def histTweets2(df):
    ax = df.tweet_created_at.groupby(level=[0]).get_group('chaco').hist(bins=100,alpha=0.5,color='red',label = 'Chaco',stacked=True)
    df.tweet_created_at.groupby(level=[0]).get_group('neuquen').hist(bins=100,ax=ax,color='green',alpha=0.5,label=u'Neuquén',stacked=True)
    ax.legend()
    ax.get_figure().savefig("{0}histTweetsProvincia2{1}{2}.pdf".format(relativePathImages,path,pathFiltro),dpi=300)
    plt.close(ax.get_figure())

def histCreated(df):
    ax = df.groupby(level=0).get_group('lapampa').drop_duplicates(subset='user_id').created_at.hist(bins=20,alpha=0.5,color='red',label = 'La Pampa')
    df.groupby(level=0).get_group('buenosaires').drop_duplicates(subset='user_id').created_at.hist(bins=20,alpha=0.5,color='green',label = 'Buenos Aires',ax=ax)
    ax.get_figure().savefig("{0}histCreated{1}{2}.pdf".format(relativePathImages,path,pathFiltro),dpi=300)
    plt.close(ax.get_figure())


if __name__ == "__main__":
    set_style()
    relativePathImages = 'latex/src/images/'

    train = True
    filtro = False
    path = '' if train else '_test'
    pathFiltro = '' if filtro else '_sinFiltro' 
    # provincias = argentina.keys()
    # frames = []
    # tknzr = TweetTokenizer(preserve_case=False,reduce_len=True, strip_handles=True)
    # parse_dates = ['tweet_created_at', 'created_at']
    # cols = ['tweet_created_at','created_at','user_id','text']
    # for p in provincias:
    #     dfT = pd.read_csv('../csv/train_{0}.csv'.format(p),usecols=cols,encoding='utf-8',delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL, parse_dates=parse_dates)
    #     dfT.fillna('',inplace=True)
    #     dfT['cantPalabras'] = dfT.text.apply(lambda x: len([w for w in tknzr.tokenize(x.lower()) if w.isalpha()])) 
    #     dfT = dfT.drop('text', 1)
    #     frames.append(dfT)
    # arg = pd.concat(frames,keys = provincias,names=['provincias','nro'])
    # arg.to_csv('contrastes/argTiemposYCant.csv')
    arg = pd.read_csv('contrastes/argTiemposYCant.csv',index_col=[0,1],parse_dates=['tweet_created_at', 'created_at'])

    cantPalabrasPromedio(arg)
    cantPalabrasUsuario(arg)
    cantTweetsUsuario(arg)
    histTweets1(arg)
    histTweets2(arg)
    histCreated(arg)