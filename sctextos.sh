#!/bin/bash

echo 'Vargo el entorno virtual'
source venv/bin/activate
echo 'Creo los directorios necesarios'
mkdir csv
mkdir train
mkdir test
cd train
mkdir listas
mkdir regiones
cd ..
echo 'Empiezo a separar los usuarios y creo dataframes de train y test'
python datosUsuarios.py
echo 'Genero los csv con los tweets por provincia de train y test'
python split_train_test.py
echo 'Tokenizo los textos y genero las listas con diferencias significativas'
python textos.py
echo 'Genero las listas de pares de regiones de forma ordenada según la máxima diferencia de ocurrencias'
python get_lines.py