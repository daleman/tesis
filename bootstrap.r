
### script para generar los pvalores a través de bootstrap
### antes de correr este script se deben generar los .csv de las provincias que indican cuantas ocurrencias
### de una palabra tiene cada usuario: python muestreoUsuarios.py

setwd("~/tesis")

# Step function
H <- function(value1, value2) {
  x = 0;
  if(value1 > value2) {
    x = 1;
  }
  if(value1 == value2) {
    x = 0.5;
  }
  x
}

# Bootstrap test
bootstraptest <- function(data1, data2, N) {
  # Compute number of elements in the shortest vector
  n <- min(length(data1),length(data2));
  
  # Compute (unnormalized) p1
  p1 = 0;
  for (i in 1:N) {
    p1 = p1 + H(mean(sample(data1,n,replace=TRUE)),mean(sample(data2,n,replace=TRUE)));
    #cat(mean(sample(data1,n,replace=TRUE)),mean(sample(data2,n,replace=TRUE)),'\n')
  }
  p1 = p1/N;
  
  # Compute p2
  p2 = (1+2*N*min(p1,1-p1))/(1+N);
  
  # Return p2
  p2
}

# el path donde se encuentran los .csv con la cantidad de ocurrencias de cada palabra por cada usuario.
# hay un csv por cada provincia, con el nombre [nombreProvincia].csv
path = '~/tesis/dataUsuarios/desarrollo/'

# listado de todas las provincias de argentina
provincias = c('jujuy',  'catamarca',  'sanjuan',  'salta',  'rionegro',  'lapampa',  'chaco',
               'mendoza',  'buenosaires',  'entrerios',  'chubut',  'santacruz',  'neuquen',
               'misiones',  'corrientes',  'formosa',  'santafe',  'santiago',  'cordoba',  'larioja',  'tierradelfuego',  'tucuman',  'sanluis')

# leo todos los .csv de cada provincia y creo variables con los dataframes de cada provincia con su nombre respectivo.
# ej. la variable buenosaires va a tener el dataframe de buenos aires
for(p in provincias){
  df = read.csv(file=paste(path,p,'.csv',sep = ''),check.names=FALSE,stringsAsFactors = FALSE,row.names = 1)
  assign(p,df)
}

# convierto un vector de nombres de provincias como una lista
vectorALista<-function(regionVector){
  lapply(X=as.list(regionVector),FUN = get)
}

# obtengo las frecuencias de ocurrencias de cada palabra por cada usuario sobre cada provincia de la region

frecuencia<-function(palabra,region){
  l = vectorALista(region)
  lapply(X=l,FUN=function(provincia){provincia[palabra,]})
}

# uno todos las frecuencias de todas las provincias de la region en una sola lista
frecuenciasRegion<-function(palabra,region){
  do.call(cbind,frecuencia(palabra,region))
}

# ivalues tiene el csv con las regiones de cada palabra. Estas regiones estan en formato de lista pero como un string
# por lo tanto se parsea
ivalues = 'notebooks/ivalue_entropia_personas_palabras.csv'
df2 <- read.csv(ivalues,stringsAsFactors = FALSE,row.names = 1)

# funcion para parsear y obtener las provincias de la palabra
region <-function(palabra){
  gsub("\\[|\\]| |'",'',unlist((strsplit(df2[palabra,"regionTest"],split = ','))))
}

# calcula el conjunto de provincias que no son parte de la region pasada por parametro 
restoPais<-function(region){
  setdiff(provincias,region)
}

# calcula la region de la palabra y el resto del pais
# luego obtiene las frecuencias en cada region y realiza el bootrstrap test a partir de esos vectores de frecuencias
pvalor<-function(palabra,N=10000){
  region1 = region(palabra)
  region2 = restoPais(region1)
  freqs1 = (frecuenciasRegion(palabra,region1))
  freqs2 = (frecuenciasRegion(palabra,region2))
  freqs1[is.na(freqs1)] = 0
  freqs2[is.na(freqs2)] = 0
  freqs1 = unlist(freqs1)
  freqs2 = unlist(freqs2)
  
  bootstraptest(data1 = freqs1,data2 = freqs2,N)
}

# obtiene la media de una palabra en el vector de provincias
media<- function(palabra,region){
  mean(lista(palabra,region))
}
# obtiene el desvio estandar de una palabra en el vector de provincias
desvio<- function(palabra,region){
  sd(lista(palabra,region))
}

# obtiene las frecuencias de todas las provincias pasadas como parametro 
lista<- function(palabra,region){
  l = vectorALista(region)
  (unlist(cbind(lapply(X=l,FUN=function(provincia){provincia[palabra,]}))))
}

#cat(paste('que',pvalor('que',N = 100000),'\n'))
#cat(paste('de',pvalor('de',N = 100000),'\n'))
#cat(paste('la',pvalor('la',N = 100000),'\n'))
#cat(paste('racing',pvalor('racing',N = 100000),'\n'))

# asigno en def el listado de palabras analizado por la AAL
def = read.csv('definitivo.csv')[1:20000,] #4999
colnames(def)[1]<- 'palabra'

# filtro unicamente las palabras seleccionadas como candidatas
#x = def[def$Palabra.Candidata ==1,'palabra']

#x = x[1:10]   # Sacar esta línea para testear sobre todas las palabras candidatas
#x = c('hola','que','de','cuando','la','el')

#Rprof()

# creo un dataframe con las palabras candidatas
#df3 = df2[is.element(row.names(df2) ,x),]

# elimino la palabra '' para evitar problemas
#df3 = df3[!(rownames(df3)==''),] # elimino del dataframe la palabra ''
df3 = df2[!(rownames(df2)==''),]
# calculo el pvalor para cada palabra candidata y lo guardo en una columna del dataframe
df3$pvalor = lapply(X = rownames(df3), FUN = function(x) { pvalor(x[1],10000)} )

# realizo la correccion por multiples test de Benjamini-Hochberg
df3$BH = p.adjust(df3$pvalor,method = 'BH')

# ordeno segun el p-valor despues de aplicar la correccion de Benjamini-Hochberg
df3 = df3[order(df3$BH),c('pvalor','BH')]
#Rprof(NULL)
#summaryRprof()
#View(df3)
df3$pvalor = unlist(df3$pvalor)
#write.csv(df3,'PbootstrapUsuarios.csv')

#df3hist(unlist(frecuenciasRegion('que',c('cordoba'))), col=rgb(1,0,0,0.5), main="Overlapping Histogram", xlab="Variable",freq = TRUE)
#hist(unlist(frecuenciasRegion('que',c('buenosaires'))), col=rgb(0,0,1,0.5),add=T)
