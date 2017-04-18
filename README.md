# Tesis de Licenciatura

## Scripts

- `users.py`: Realiza una búsqueda de usuarios de twitter en la provincia indicada por parámetro.  


- `datosUsuarios.py`: Separa el conjunto de train de test. Guarda los datos de train en `train/` y los de test en `test/`  

- `textos.py`: Tokeniza todos los tweets y arma un listado de palabras por provincia con su cantidad de ocurrencias, fnorm y pvalor del ztest entre la cantidad de ocurrencias de cada palabra entre par de provincias. Separa los conjuntos de palabras por regiones dialectales.

-  `getlines.py`: Genera el csv con la columna maxDif que representa la máxima diferencia de frecuencias normalizadas para cada palabra.


## Datos

- `tweets/`: todos los tweets, en arrays de `json`. Datos crudos

Los archivos `*_tweets.json` tienen los tweets segmentados por provincia.
Los archivos `.dat` indican la cantidad acumulada de tweets según voy agregando usuarios (podemos ignorarlos)

- `train/` tiene los datos de entrenamiento/discovery.

`train_provincia.csv` tiene los tweets reducidos de la siguiente manera:

tweet_id, user_id, text

`train_provincia_dict.json` tiene el bag of words de los tweets
`train_provincia_users_dict.json` tiene un diccionario de palabras a `user_ids` (los que usaron dicha palabra)

- `test/` tiene los datos de validación, pero sólo en formato `csv` (lo demás no lo hicimos)