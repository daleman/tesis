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
    ax.get_figure.savefig("{0}cantPalabrasPromedio.pdf".format(relativePathImages),dpi=300)
    plt.close(ax.get_figure())

def cantPalabrasPorUsuario(df):
    ax = sns.distplot(df.groupby('user_id').cantPalabras.sum(),hist=True,kde=False)
    ax.set_xlabel('Cantidad de palabras por usuario')
    ax.get_figure.savefig("{0}cantPalabrasUsuario.pdf".format(relativePathImages),dpi=300)
    plt.close(ax.get_figure())

def cantTweetsPorUsuario(df):
    ax = sns.distplot(arg.groupby('user_id').cantPalabras.count(),hist=True,kde=False)
    ax.set_xlabel(u'Cantidad de tweets por usuario')
    ax.get_figure.savefig("{0}cantTweetsUsuario.pdf".format(relativePathImages),dpi=300)
    plt.close(ax.get_figure())

def histTweets1(df):
    ax = df.tweet_created_at.groupby(level=[0]).get_group('lapampa').hist(bins=100,alpha=0.5,color='red',label = 'La Pampa',stacked=True)
    arg.tweet_created_at.groupby(level=[0]).get_group('buenosaires').hist(bins=100,ax=ax,color='green',alpha=0.5,label='Buenos Aires',stacked=True)
    ax.legend()
    ax.get_figure().savefig("{0}histTweetsProvincia{1}.pdf".format(relativePathImages),dpi=300)
    plt.close(ax.get_figure())

def histTweets2(df):
    ax = df.tweet_created_at.groupby(level=[0]).get_group('chaco').hist(bins=100,alpha=0.5,color='red',label = 'Chaco',stacked=True)
    arg.tweet_created_at.groupby(level=[0]).get_group('neuquen').hist(bins=100,ax=ax,color='green',alpha=0.5,label=u'Neuquén',stacked=True)
    ax.legend()
    ax.get_figure().savefig("{0}histTweetsProvincia2.pdf".format(relativePathImages),dpi=300)
    plt.close(ax.get_figure())

def histCreated(df):
    ax = df.groupby(level=0).get_group('lapampa').drop_duplicates(subset='user_id').created_at.hist(bins=20,alpha=0.5,color='red',label = 'La Pampa')
    df.groupby(level=0).get_group('buenosaires').drop_duplicates(subset='user_id').created_at.hist(bins=20,alpha=0.5,color='green',label = 'Buenos Aires',ax=ax)
    plt.close(ax.get_figure())


if __name__ == "__main__":
    set_style()
    relativePathImages = 'latex/src/images/'
    provincias = argentina.keys()
    frames = []
    for p in provincias:
        dfT = pd.read_csv('csv/train_{0}.csv'.format(p),encoding='utf-8',delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        dfT.tweet_created_at = pd.to_datetime(dfT.tweet_created_at)
        dfT.created_at = pd.to_datetime(dfT.created_at)
        frames.append(dfT)
    arg = pd.concat(frames,keys = provincias,names=['provincias','nro'])
    tknzr = TweetTokenizer(preserve_case=False,reduce_len=True, strip_handles=True)
    arg['cantPalabras'] = arg.text.apply(lambda x: len([w for w in tknzr.tokenize(x.lower()) if w.isalpha()]))

    cantPalabrasPromedio(arg)
    cantPalabrasPorUsuario(arg)
    cantTweetsUsuario(arg)
    histTweets1(arg)
    histTweets2(arg)
    histCreated(arg)