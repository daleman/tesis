#!/bin/bash

cd ~/tesis

# crea el directorio si no existe
echo "Creo directorio"
mkdir -p dataUsuarios 

echo "genero los .csv"
# genero los .csv que tienen la cantidad de ocurrencias de cada palabra por cada usuario por provincia
python muestroUsuarios.py

echo "bootstrap test"
# hago el test de bootstrap con las palabras definitivas
Rscript bootstrap.r
echo "terminaron los tests"