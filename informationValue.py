# coding: utf-8
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import nltk
import re
from scipy.stats import entropy
from iv_helpers import simulated_shuffled_entropy_multinomial
import argparse

sns.set_style("whitegrid")
relativePathImages = 'latex/src/images/'


def lugares():
    with open('localidades/cabeceras.geojson') as cab,\
            open('localidades/capitales.geojson') as cap,\
            open('localidades/localidades.geojson') as loc,\
            open('localidades/departamentos.geojson') as dep:
        cabeceras = json.load(cab)
        capitales = json.load(cap)
        localidades = json.load(loc)
        departamentos = json.load(dep)
        lugares = set([])
        for a in [cabeceras, capitales, localidades, departamentos]:
            for n in a['features']:
                for w in nltk.word_tokenize(n['properties']['nombre']):
                    lugares.add(w.lower())

    return lugares

def propAcumLinea(percent,palabras):
    dfAcum = pd.DataFrame()
    dfAcum['1000'] = percent.iloc[:1000].cumsum(axis=1).mean()
    dfAcum['2000'] = percent.iloc[:2000].cumsum(axis=1).mean()
    dfAcum['5000'] = percent.iloc[:5000].cumsum(axis=1).mean()
    dfAcum['10000'] = percent.iloc[:10000].cumsum(axis=1).mean()
    dfAcum['Candidatas AAL'] = percent.loc[palabras].cumsum(axis=1).mean()
    dfAcum['Todas'] = percent.cumsum(axis=1).mean()
    ax = dfAcum.plot(kind='line')
    ax.set_xlabel(u"Cantidad de provincias")
    ax.set_ylabel(u"Proporción acumulada")
    ax.get_figure().savefig("{0}PropAcum{1}.pdf".format(relativePathImages,path), dpi=300)
    plt.close(ax.get_figure())

def propAcum5000(percent):
    ax2 = percent.iloc[:5000].cumsum(axis=1).boxplot(return_type='axes')
    ax2.set_xlabel(u"Cantidad de provincias")
    ax2.set_ylabel(u"Proporción acumulada")
    ax2.get_figure().savefig("{0}PropAcum5000{1}.pdf".format(relativePathImages,path),dpi=300)


if __name__ == "__main__":


    parser = argparse.ArgumentParser()
    parser.add_argument("trainOTest", help="Indicar si querés analizar el conjunto de train o de test",
                        type=str)

    args = parser.parse_args()
    trainOTest = args.trainOTest

    path = '_test' if (trainOTest.lower() =='test') else ''

    print('cargo el dataframe')

    df = pd.read_csv("contrastes/provincias{0}.csv".format(path),index_col=0)

    fnorm_vars = [c for c in df.columns if re.match(r'fnorm_.*', c)]
    cant_palabras = [c for c in df.columns if re.match(r'.*Palabras$', c)]
    cant_personas = [c for c in df.columns if re.match(r'.*Personas$', c)]


    fn = lambda ws: simulated_shuffled_entropy_multinomial(ws, len(cant_palabras))
    print('calculo la entropia y los valores de información')
    df["entropy_palabras"] = df[cant_palabras].apply(entropy, axis=1, raw=True)
    df["entropy_personas"] = df[cant_personas].apply(entropy, axis=1, raw=True)
    df["shuffled_entropy_personas"] = df.cantUsuariosTotal.apply(fn)
    df["shuffled_entropy_palabras"] = df.cantPalabra.apply(fn)
    cantPalabrasTotales = sum(df.cantPalabra)
    df['fnormArgentina'] = df['cantPalabra'] / cantPalabrasTotales


    df['normCantPalabras'] = (df.cantPalabra.apply(math.log, args=(2,)) - df.cantPalabra.apply(math.log, args=(2,)).min()) / \
        (df.cantPalabra.apply(math.log, args=(2,)).max() -
         df.cantPalabra.apply(math.log, args=(2,)).min())
    df['normCantPersonas'] = (df.cantUsuariosTotal.apply(math.log, args=(2,)) - df.cantUsuariosTotal.apply(math.log, args=(2,)).min()) / \
        (df.cantUsuariosTotal.apply(math.log, args=(2,)).max() -
         df.cantUsuariosTotal.apply(math.log, args=(2,)).min())

    places = lugares()
    df['esLugar'] = np.where(df.index.str.decode(
        encoding='utf-8').isin(places), 'lugar', 'ok')

    df["information_value_palabras"] = (df.cantPalabra.apply(
        math.log, args=(2,))) * (df.shuffled_entropy_palabras - df.entropy_palabras)
    df["information_value_personas"] = (df.cantPalabra.apply(
        math.log, args=(2,))) * (df.shuffled_entropy_personas - df.entropy_personas)
    df["information_value_personas_palabras"] = df.normCantPalabras * df.normCantPersonas * \
        (df.shuffled_entropy_personas - df.entropy_personas) * \
        (df.shuffled_entropy_palabras - df.entropy_palabras)

    print('ordeno el dataframe según el valor de información')
    df.sort_values(by="information_value_personas_palabras",
                   ascending=False, inplace=True)
    df['rankPalabras'] = df['information_value_palabras'].rank(
        ascending=False).astype('int64')
    df['rankPersonas'] = df['information_value_personas'].rank(
        ascending=False).astype('int64')
    df['rankPalabras_Personas'] = df['information_value_personas_palabras'].rank(
        ascending=False).astype('int64')


    palabrasPersonas = [
        c for c in df.columns if re.match(r'.*PalabrasPersonas', c)]
    resumed = df[df.columns.difference(
        cant_palabras + fnorm_vars + palabrasPersonas)]
    # df.iloc[:1000][['fnormArgentina','cantPalabra','esLugar','cantUsuariosTotal','provinciaFnormMax','rankPalabras','rankPersonas','rankPalabras_Personas','normCantPersonas','normCantPalabras','shuffled_entropy_personas','entropy_personas']]

    cant = [c for c in df.columns if re.match(
        r'.*Palabras$', c) and (not re.match(r'.*norm', c)) and (not re.match(r'.*rank', c))]

    dfCant = df[cant]
    # Palabras candidatas según la AAL
    palabras = ["quedarla", "mitaí", "angá", "yungas", "mensajeras", "yarco", "yarca",
                "malpegar", "malpegue", "malpegada", "tareferos", "hartante", "guaracha", "esar", "ñeri",
                "piadina", "chombi", "achilata", "pollerear", "juntadera", "pachata", "chamigo", "chamiga",
                "chaque", "pichar", "tortita", "guaso", "guasa", "comparsero", "comparsera", "sina", "lape", "veme", "porronear",
                "fajita", "jia", "jía", "asada", "asar", "manso", "cora", "cumpa", "pingo", "charro", "pinchila", "oyo", "ura", "yuto",
                "yagua", "cantobar", "cha", "bombolo", "bombola", "yafu", "jal", "gatera", "atina",
                "guampudo", "guampuda", "mamila", "chui", "tico"]

    # Ordeno las proporciones de las provincias por cada palabra, de modo tal que tenga por cada palabra
    # las proporciones ordenadadas de mayor a menor
    dfC = df.sort_values(by="information_value_personas_palabras",
                         ascending=False, inplace=False)[cant]
    sort_xs = dfC.apply(np.sort, axis=1)
    sort_index = dfC.apply(np.argsort, axis=1)
    sort_xs.columns = range(23)
    sort_index.columns = range(23)
    cols = sort_xs.columns.tolist()
    cols = cols[::-1]
    sort_xs = sort_xs[cols]
    sort_index = sort_index[cols]
    sort_xs.columns = range(23)
    sort_index.columns = range(23)

    percent = sort_xs.div(sort_xs.sum(axis=1), axis='index')

    # Proporciones acumuladas linea
    print('gráfico linea')
    propAcumLinea(percent,palabras)

    # Proporciones acumuladas boxplot
    print('gráfico proporciones acumuladas boxplot')
    propAcum5000(percent)

    provincias = [x.replace("Palabras","") for x in cant]
    regiones = pd.DataFrame()
    regiones = percent.cumsum(axis=1)
    def provs(row, thresh):
        for i in range(len(row)):
            if row[i] > thresh:
                cant = sort_index.loc[row.name].iloc[:i + 1].tolist()
                return [provincias[x] for x in cant]
    df['regionTest'] = regiones.apply(provs, args=(0.8,), axis=1)

    dfR = pd.read_csv('cantidadesDataset{0}.csv'.format(path),index_col=0)

    def cantPalabrasTotalesEnRegion(provincias):
        return sum(dfR.loc[provincias,'cantTotal'])

    def cantPalabrasWEnRegion(palabra,provincias):
        provs = [p+'Palabras' for p in provincias]
        return sum(df.loc[palabra,provs])

    print('calculo las cantidades en las regiones')
    df['cantPalabrasTotalesEnRegion'] = df.regionTest.apply(cantPalabrasTotalesEnRegion)
    df['cantPalabrasWEnRegion'] = df.apply(lambda x: cantPalabrasWEnRegion(x.name,x.regionTest),axis=1)

    print('guardo el dataframe en un csv')
    df.sort_values(by="information_value_personas_palabras", ascending=False, inplace=True)
    resumed = df[df.columns.difference(cant_palabras+fnorm_vars + palabrasPersonas)]
    resumed = resumed[['cantPalabra','esLugar','regionTest','cantUsuariosTotal','fnormArgentina','provinciaFnormMax','rankPalabras','rankPersonas','rankPalabras_Personas','cantPalabrasWEnRegion','cantPalabrasTotalesEnRegion']]
    resumed.to_csv('ivalue_entropia_personas_palabras_resumida{0}.csv'.format(path))

    df.to_csv('ivalue_entropia_personas_palabras{0}.csv'.format(path))