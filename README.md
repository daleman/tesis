# tesis


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