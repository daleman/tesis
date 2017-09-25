
### script para generar los pvalores a través de bootstrap
### antes de correr este script se deben generar los .csv de las provincias que indican cuantas ocurrencias
### de una palabra tiene cada usuario

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

path = '~/tesis/dataUsuarios/'


provincias = c('jujuy',  'catamarca',  'sanjuan',  'salta',  'rionegro',  'lapampa',  'chaco',
               'mendoza',  'buenosaires',  'entrerios',  'chubut',  'santacruz',  'neuquen',
               'misiones',  'corrientes',  'formosa',  'santafe',  'santiago',  'cordoba',  'larioja',  'tierradelfuego',  'tucuman',  'sanluis')

for(p in provincias){
  df = read.csv(file=paste(path,p,'.csv',sep = ''),check.names=FALSE,row.names = 1)
  assign(p,df)
}
vectorALista<-function(regionVector){
  lapply(X=as.list(regionVector),FUN = get)
}

frecuencia<-function(palabra,region){
  l = vectorALista(region)
  lapply(X=l,FUN=function(provincia){provincia[palabra,]})
}

frecuenciasRegion<-function(palabra,region){
  do.call(cbind,frecuencia(palabra,region))
}

ivalues = 'notebooks/ivalue_entropia_personas_palabras.csv'
df2 <- read.csv(ivalues,stringsAsFactors = FALSE,row.names = 1)

region <-function(palabra){
  gsub("\\[|\\]| |'",'',unlist((strsplit(df2[palabra,"regionTest"],split = ','))))
}

restoPais<-function(region){
  setdiff(provincias,region)
}

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


media<- function(palabra,region){
  mean(lista(palabra,region))
}
desvio<- function(palabra,region){
  sd(lista(palabra,region))
}

lista<- function(palabra,region){
  l = vectorALista(region)
  (unlist(cbind(lapply(X=l,FUN=function(provincia){provincia[palabra,]}))))
}

#cat(paste('que',pvalor('que',N = 100000),'\n'))
#cat(paste('de',pvalor('de',N = 100000),'\n'))
#cat(paste('la',pvalor('la',N = 100000),'\n'))
#cat(paste('racing',pvalor('racing',N = 100000),'\n'))

def = read.csv('definitivo.csv')[1:100,] #4999
colnames(def)[1]<- 'palabra'
x = def[def$Palabra.Candidata ==1,'palabra']
#x = x[1:10]   # Sacar esta línea para testear sobre todas las palabras candidatas
#x = c('hola','que','de','cuando','la','el')

df3 = df2[is.element(row.names(df2),x),]
df3$palabra = rownames(df3)
df3$pvalor = lapply(X = rownames(df3), FUN = function(x) { pvalor(x[1])} )
df3 = df3[,c('pvalor','regionTest')]
df3$BH = p.adjust(df3$pvalor,method = 'BH')
df3 = df3[order(df3$BH),c('pvalor','BH')]
write.csv(df3,'PbootstrapUsuarios.csv')
#df3hist(unlist(frecuenciasRegion('que',c('cordoba'))), col=rgb(1,0,0,0.5), main="Overlapping Histogram", xlab="Variable",freq = TRUE)
#hist(unlist(frecuenciasRegion('que',c('buenosaires'))), col=rgb(0,0,1,0.5),add=T)
