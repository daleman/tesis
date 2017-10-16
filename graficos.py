# coding: utf-8

from apps import argentina
import csv
from nltk.tokenize import TweetTokenizer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
from statsmodels.sandbox.stats.multicomp import multipletests


def set_style():
    plt.style.use(['seaborn-paper', 'seaborn-white'])
    plt.rc("font", family="Times New Roman")


def cantPalabrasPromedio(df):
    cantPalMedia = df.groupby('user_id').cantPalabras.mean()
    ax = sns.distplot(a=cantPalMedia, hist=True, kde=False, bins=100)
    ax.set_xlabel(u'Cantidad de palabras promedio por usuario')
    ax.set_ylabel(u'Cantidad de usuarios')
    fig = ax.get_figure()
    fig.savefig("{0}cantPalabrasPromedio{1}{2}.pdf".format(
        relativePathImages, path, pathFiltro), dpi=300)
    plt.close(fig)


def cantPalabrasUsuario(df):
    ax = sns.distplot(df.groupby(
        'user_id').cantPalabras.sum(), hist=True, kde=False)
    ax.set_xlabel(u'Cantidad de palabras por usuario')
    ax.set_ylabel(u'Cantidad de usuarios')
    fig = ax.get_figure()
    fig.savefig("{0}cantPalabrasUsuario{1}{2}.pdf".format(
        relativePathImages, path, pathFiltro), dpi=300)
    plt.close(fig)


def cantTweetsUsuario(df):
    ax = sns.distplot(df.groupby(
        'user_id').cantPalabras.count(), hist=True, kde=False)
    ax.set_xlabel(u'Cantidad de tuits por usuario')
    ax.set_ylabel(u'Cantidad de usuarios')
    fig = ax.get_figure()
    fig.savefig("{0}cantTweetsUsuario{1}{2}.pdf".format(
        relativePathImages, path, pathFiltro), dpi=300)
    plt.close(fig)


def histTweets1(df):
    # ax = df.tweet_created_at.groupby(level=[0]).get_group('lapampa').hist(
    #     bins=100, alpha=0.5, color='red', label='La Pampa', stacked=True)
    # df.tweet_created_at.groupby(level=[0]).get_group('buenosaires').hist(
    #     bins=100, ax=ax, color='green', alpha=0.5, label='Buenos Aires', stacked=True)
    ax = sns.distplot(df.tweet_created_at.groupby(level=[0]).get_group('lapampa'),bins=100, kde=False, rug=False, color='red', label='La Pampa')
    sns.distplot(df.tweet_created_at.groupby(level=[0]).get_group('buenosaires'),bins=100,  kde=False, rug=False, color='green', label='Buenos Aires',ax=ax)
    
    ax.set_xlabel(u'Año')
    ax.set_ylabel(u'Cantidad de tuits')
    ax.legend()
    fig = ax.get_figure()
    fig.savefig("{0}histTweetsProvincia1{1}{2}.pdf".format(
        relativePathImages, path, pathFiltro), dpi=300)
    plt.close(fig)


def histTweets2(df):
    # ax = df.tweet_created_at.groupby(level=[0]).get_group('chaco').hist(
    #     bins=100, alpha=0.5, color='red', label='Chaco', stacked=True)
    # df.tweet_created_at.groupby(level=[0]).get_group('neuquen').hist(
    #     bins=100, ax=ax, color='green', alpha=0.5, label=u'Neuquén', stacked=True)
    ax = sns.distplot(df.tweet_created_at.groupby(level=[0]).get_group('chaco'),bins=100, kde=False, rug=False, color='red', label='Chaco')
    sns.distplot(df.tweet_created_at.groupby(level=[0]).get_group('neuquen'),bins=100, kde=False, rug=False, color='green', label=u'Neuquén',ax=ax)
    ax.set_xlabel(u'Año')
    ax.set_ylabel(u'Cantidad de tuits')
    ax.legend()
    fig = ax.get_figure()
    fig.savefig("{0}histTweetsProvincia2{1}{2}.pdf".format(
        relativePathImages, path, pathFiltro), dpi=300)
    plt.close(fig)


def histCreated(df):
    # ax = df.groupby(level=0).get_group('lapampa').drop_duplicates(
    #     subset='user_id').created_at.hist(bins=100, alpha=0.5, color='red', label='La Pampa')
    # df.groupby(level=0).get_group('buenosaires').drop_duplicates(subset='user_id').created_at.hist(
    #     bins=100, alpha=0.5, color='green', label='Buenos Aires', ax=ax)

    ax = sns.distplot(df.groupby(level=0).get_group('lapampa').drop_duplicates(subset='user_id').created_at,bins=100, kde=False, rug=False, color='red', label='La Pampa')
    sns.distplot(df.groupby(level=0).get_group('buenosaires').drop_duplicates(subset='user_id').created_at,bins=100, kde=False, rug=False, color='green', label='Buenos Aires',ax=ax)

    ax.legend()
    fig = ax.get_figure()
    fig.savefig("{0}histCreated{1}{2}.pdf".format(
        relativePathImages, path, pathFiltro), dpi=300)
    plt.close(fig)


def ivaluesLog(df):
    df2 = df.sort_values(
        by="information_value_personas_palabras", ascending=False)
    df2 = df2.reset_index()
    ax2 = df2.information_value_personas_palabras.plot(logx=True)
    ax2.set_xlabel(u'Posición de palabra')
    ax2.set_ylabel(u'Valor de la inforamción')
    fig = ax2.get_figure()
    fig.savefig("{0}ivaluesLog{1}{2}.pdf".format(
        relativePathImages, path, pathFiltro), dpi=300)
    plt.close(fig)


def zipf(df):
    df2 = df.sort_values(by='cantPalabra', ascending=False, inplace=False)
    df2['Rank'] = df2['cantPalabra'].rank(method='min', ascending=False)
    x = range(len(df2.cantPalabra))
    x = np.log(df2['Rank'])
    y = np.log(df2['cantPalabra'])
    fit = np.polyfit(x, y, deg=1)
    fitted = fit[0] * x + fit[1]
    print 'Valor estimado de s:\n{0}'.format(fit[0])
    fig = plt.Figure(figsize=(4, 4), facecolor='w', edgecolor='w')
    ax = plt.subplot(111)

    ax.plot(x, y, 'bo', alpha=0.5)
    ax.plot(x, fitted, 'r')
    ax.set_xlabel(u'Log(Posición de palabra en el listado ordenado)')
    ax.set_ylabel(u'Log(Cantidad de ocurrencias de palabra)')
    ax.set_xlim(left=max([min(np.log(df2['Rank'])) * 0.95, 0]))
    # for i, txt in enumerate(df2.iloc[:10].index,):
    #     ax.annotate(txt, (x[i],y[i]))
    fig = ax.get_figure()
    fig.savefig("{0}zipf{1}{2}.pdf".format(
        relativePathImages, path, pathFiltro), dpi=300)
    plt.close(fig)


def entropyVsNormCantPersonas(df):
    df.sort_values(by="information_value_personas",
                   ascending=False, inplace=False)
    # df[u'Posición en listado ordenado ']
    ax = df.iloc[:10000].plot(kind='scatter', x='entropy_personas', y='normCantPersonas',
                              c='rankPalabras_Personas', sharex=False, cmap='Reds', alpha=0.5)
    ax.set_xlabel(u'$H_p$: Entropía en base a la cantidad de personas')
    ax.set_ylabel(u'$norm_p$')
    fig = ax.get_figure()
    fig.get_axes()[1].set_ylabel(u'Posición en el listado ordenado por I')
    fig.savefig("{0}entropiaPersonasxNormCantPersonas{1}{2}.pdf".format(
        relativePathImages, path, pathFiltro), dpi=300)
    plt.close(fig)


def distribucionEntropia(df):
    ax = sns.distplot(a=df.entropy_palabras, hist=True, kde=False,
                      axlabel=u'$H_w$: Entropía de la cantidad de palabras', bins=100)
    ax.set_yscale('log')
    fig = ax.get_figure()
    fig.savefig("{0}DistribucionEntropia{1}{2}.pdf".format(
        relativePathImages, path, pathFiltro), dpi=300)
    plt.close(fig)


def distCantPalabra(df):
    ax = sns.distplot(a=df.cantPalabra, hist=True, bins=40, kde=False)
    ax.set_yscale('log')
    ax.set_xlabel('Cantidad de ocurrencias por palabra')
    ax.set_ylabel('Cantidad de palabras')
    fig = ax.get_figure()
    fig.savefig("{0}DistribucionOcurrenciasPalabras{1}{2}.pdf".format(
        relativePathImages, path, pathFiltro), dpi=300)
    plt.close(fig)


def rankIValue(df):
    ax = df.plot(x='rankPalabras_Personas',
                 y='information_value_personas_palabras', logx=True, legend=False)
    ax.axvline(4000, linestyle='--', color='k')
    ax.set_xlabel(u'Posición en el listado ordenado')
    ax.set_ylabel(u'Valor de la información')
    fig = ax.get_figure()
    fig.savefig("{0}valorInformacionCorte{1}{2}.pdf".format(
        relativePathImages, path, pathFiltro), dpi=300)
    plt.close(fig)


def originalVsShuffle(df):
    df2 = pd.DataFrame()
    df2['x'] = df.cantPalabra
    df2['y'] = df.entropy_palabras
    ax = df2.plot(kind='scatter', x='x', y='y', s=5,
                  color='black', logx=True, label=u'Texto original')

    df3 = pd.DataFrame()
    df3['x'] = df.cantPalabra
    df3['y'] = df.shuffled_entropy_palabras
    df3.plot(kind='scatter', x='x', y='y', s=5, color='gray',
             logx=True, ax=ax, label=u'Versión reordenada')
    ax.set_xlabel(u'Cantidad de ocurrencias de palabra')
    ax.set_ylabel(u'Entropía de Palabras')
    ax.legend()
    fig = ax.get_figure()
    fig.savefig("{0}entropiaYversionShuffleada{1}{2}.pdf".format(
        relativePathImages, path, pathFiltro), dpi=300)
    plt.close(fig)


def cantNorms(df):
    sns.set_context('paper')
    fig, axes = plt.subplots(ncols=2, nrows=2, sharey=True)
    sns.distplot(df.cantUsuariosTotal, kde=False, ax=axes[0, 0])
    sns.distplot(df.normCantPersonas, kde=False, ax=axes[0, 1])
    sns.distplot(a=df.cantPalabra, kde=False, ax=axes[1, 0])
    sns.distplot(df.normCantPalabras, kde=False, ax=axes[1, 1])
    fig.subplots_adjust(hspace=.4)
    # axes[0,0].set(xlabel='Cantidad de ocurrencias', ylabel='')
    replacements = {'cantUsuariosTotal': 'Cantidad de usuarios total', 'normCantPersonas': r'$norm_p$',
                    'cantPalabra': 'Cantidad de ocurrencias de Palabra', 'normCantPalabras': r'$norm_w$'}

    axes[0, 0].set_yscale('log')

    axes[1, 0].set_yscale('log')

    for i in range(2):
        for j in range(2):
            xlabel = axes[i][j].get_xlabel()
            ylabel = axes[i][j].get_ylabel()
            if xlabel in replacements.keys():
                axes[i][j].set_xlabel(replacements[xlabel])
            if ylabel in replacements.keys():
                axes[i][j].set_ylabel(replacements[ylabel])
    fig.savefig("{0}cantNorms{1}{2}.pdf".format(
        relativePathImages, path, pathFiltro), dpi=300)


def cantNorms1(df):
    sns.set_context('paper')
    ax = sns.distplot(df.cantUsuariosTotal, kde=False)
    ax.set_yscale('log')
    ax.set_xlabel('Cantidad de usuarios que utilizan una palabra')
    ax.set_ylabel('Cantidad de palabras')
    fig = ax.get_figure()
    fig.savefig("{0}cantUsuarios{1}{2}.pdf".format(
        relativePathImages, path, pathFiltro), dpi=300)
    plt.close(fig)


def cantNorms2(df):
    sns.set_context('paper')
    ax = sns.distplot(df.normCantPersonas, kde=False)
    ax.set_yscale('log')
    ax.set_xlabel(r'$norm_p$')
    ax.set_ylabel('Cantidad de palabras')
    fig = ax.get_figure()
    fig.savefig("{0}cantNormUsuarios{1}{2}.pdf".format(
        relativePathImages, path, pathFiltro), dpi=300)
    plt.close(fig)


def cantNorms3(df):
    sns.set_context('paper')
    ax = sns.distplot(df.cantPalabra, kde=False,bins=40)
    ax.set_yscale('log')
    ax.set_xlabel('Cantidad de ocurrencias de una palabra')
    ax.set_ylabel('Cantidad de palabras')
    fig = ax.get_figure()
    fig.savefig("{0}cantPalabras{1}{2}.pdf".format(
        relativePathImages, path, pathFiltro), dpi=300)
    plt.close(fig)


def cantNorms4(df):
    sns.set_context('paper')
    ax = sns.distplot(df.normCantPalabras, kde=False)
    ax.set_yscale('log')
    ax.set_xlabel(r'$norm_w$')
    ax.set_ylabel('Cantidad de palabras')
    fig = ax.get_figure() 
    fig.savefig("{0}cantNormPalabras{1}{2}.pdf".format(
        relativePathImages, path, pathFiltro), dpi=300)
    plt.close(fig)

def palabrasIndices(indice_menor, indice_mayor,metrica,df):
    return ((df[metrica]>=indice_menor) & (df[metrica] < indice_mayor))

def variacionRechazoEnIntervalos(df,df2):

    m = 'rankPalabras_Personas'
    fig, axs = plt.subplots(nrows=1,ncols=3,sharey=True,figsize = (10*1.61803399,10))
    sns.distplot(df.pvalorWelch.loc[palabrasIndices(0,5000,m,df2)], hist=True,bins=100, kde=False,ax=axs[0])
    sns.distplot(df.pvalorWelch.loc[palabrasIndices(20000,250000,m,df2)], hist=True,bins=100, kde=False,ax=axs[1])
    sns.distplot(df.pvalorWelch.loc[palabrasIndices(50000,55000,m,df2)], hist=True,bins=100, kde=False,ax=axs[2])
    fig.subplots_adjust(hspace=.2)
    fig.subplots_adjust(wspace=.15)
    for ax in axs.flatten():
        ax.set_xlabel("p-valor",fontsize=16)
        ax.set_ylabel("Cantidad",fontsize=16)
        #     ax.set_xlim([0,1])
        ax.set_yscale('log')
        #     ax.axvline(0.05, color='black')
    fig.savefig('latex/src/images/pvalores_sinCorrecion.pdf', bbox_inches='tight',dpi=300)

def rechazoDistintasMetricas(todas_df,df2):
    metricas = ["rankPalabras_Personas","rankPalabras","rankPersonas"]
    ranges = [(i,i+5000) for i in range(0,len(df2),5000)]
    tasas = {}
    for m in metricas:
        tasas[m] = {}
    for i,j in ranges:
    #     print('\n')
        for m in metricas:
            tasa_r = (todas_df.loc[palabrasIndices(i,j,m,df2)].rechazo_H0).mean()*100
            indices = str(i) + ":" + str(j)
            tasas[m][indices] = tasa_r
    #         print("Tasa de rechazo para las palabras entre {0}:{1} según la metrica {2}: {3}".format(i,j,m,tasa_r))
    tasas_df = pd.DataFrame(tasas,columns=tasas.keys())
    tasas_df.sort_values(by='rankPalabras_Personas',ascending=False,inplace=True)


    ax = tasas_df.plot(figsize=(10*1.61803399,10),fontsize=12)
    # ax.set_title(u"Tasa de rechazo de H0 según métricas",fontsize=20)

    ax.set_ylabel("Porcentaje de rechazo",fontsize=20)
    ax.set_xlabel(u"Índices de palabras del listado ordenado",fontsize=20)
    ax.legend(fontsize=15)
    ax.get_figure().savefig('latex/src/images/rechazo_metricas.pdf', bbox_inches='tight')

if __name__ == "__main__":
    set_style()
    relativePathImages = 'latex/src/images2/'

    parser = argparse.ArgumentParser()
    parser.add_argument("trainOTest", help="Indicar si querés analizar el conjunto de train o de test",
                        type=str)
    parser.add_argument("conFiltro", help="Indicar si querés analizar los datos filtrados por la cantidad o no",
                        type=str)

    args = parser.parse_args()
    trainOTest = args.trainOTest
    filtro = args.conFiltro

    pathFiltro = '' if (filtro.lower() == 'confiltro') else '_sinFiltro'
    path = '_test' if (trainOTest.lower() == 'test') else ''

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
    
    
    df = pd.read_csv('contrastes/argTiemposYCant.csv',
                      index_col=[0, 1], parse_dates=['tweet_created_at', 'created_at'])

    
    cantPalabrasPromedio(df)
    cantPalabrasUsuario(df)
    cantTweetsUsuario(df)
    histTweets1(df)
    histTweets2(df)
    histCreated(df)

    df = pd.read_csv(
        'notebooks/ivalue_entropia_personas_palabras{0}.csv'.format(path), index_col=0)
    
    ivaluesLog(df)
    zipf(df)
    distribucionEntropia(df)
    distCantPalabra(df)
    rankIValue(df)
    originalVsShuffle(df)
    cantNorms1(df)
    cantNorms2(df)
    cantNorms3(df)
    cantNorms4(df)
    entropyVsNormCantPersonas(df)

    #cargo el dataframe con el resultado de haber aplicado welch a todas las palabras
    
    ivalues = 'notebooks/ivalue_entropia_personas_palabras.csv'
    df2 = pd.DataFrame.from_csv(ivalues,header=0,encoding='utf-8')
    todas_df = pd.DataFrame.from_csv("testEstadisticos/welchTest.csv",encoding='utf-8')
    p_adjusted = multipletests(todas_df.pvalorWelch, method='bonferroni')
    todas_df["p_adjusted"] = p_adjusted[1]
    todas_df["rechazo_H0"] = p_adjusted[0]

    tasa_rechazoH0 = todas_df.rechazo_H0.mean()*100
    # print("La tasa de rechazo de sobre todas las palabras CON la correción de Bonferroni es de {0}".format(tasa_rechazoH0))
    # print("La tasa de rechazo de sobre todas las palabras SIN la correción de Bonferroni es de {0}".format((todas_df.pvalorWelch<0.05).mean()*100))

    variacionRechazoEnIntervalos(todas_df,df2)
    rechazoDistintasMetricas(todas_df,df2)

