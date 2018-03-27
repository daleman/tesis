# coding: utf-8

import csv
import pandas as pd
import json

definitivoDifusion = pd.read_csv("cantidadesDatasetFiltrado.csv",index_col=0,encoding='utf-8')
definitivoDifusionFiltrado = definitivoDifusion[(definitivoDifusion.cantPalabra>40) & (definitivoDifusion.cantUsuariosTotal>5)]
usadoEnTesis = pd.read_csv('../contrastes/provincias.csv',index_col=0,encoding='utf-8')

print('La cantidad de ocurrencias minima en usadoEnTesis: {}'.format(usadoEnTesis.cantPalabra.min()))
print('La cantidad de usuarios minima que dicen una palabra en usadoEnTesis: {}'.format(usadoEnTesis.cantUsuariosTotal.min()))
definitivoDifusionFiltrado = definitivoDifusion[(definitivoDifusion.cantPalabra>40) & (definitivoDifusion.cantUsuariosTotal>5)]
definitivoDifusionFiltrado.index.names = ['palabra']
definitivoDifusionFiltrado = definitivoDifusionFiltrado.sort_index()
print(definitivoDifusionFiltrado.index.difference(usadoEnTesis.index))
print("La diferencia: {}".format(definitivoDifusionFiltrado.cantPalabra.ne(usadoEnTesis.cantPalabra).sum()))

defi = definitivoDifusionFiltrado.cantPalabra
usa = usadoEnTesis.cantPalabra
df = pd.DataFrame({'defi':defi,'usa':usa})
df['diferencia'] = df.defi-df.usa

print(df[df.diferencia!=0].diferencia.describe())