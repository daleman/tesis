

# cantidadesDataset tiene las cantidades de palabras totales por provincia

# cantPorProv tiene informacion mas detallada incluyendo la cantidad de ocurrencias
# de cada palabra en cada provincia

# ivalues tiene la cantidad de ocurrencias de una palabra en la region que cubre el 80 % de ocurrencias
# y tambien la cantidad de ocurrencias de la palabra en toda la argentina (para todas las palabras)

setwd("~/tesis")

testOrTrain = 'validacion'
if (testOrTrain == 'desarrollo'){
  cantidadesDataset = 'cantidadesDataset.csv'
  cantPorProv = 'contrastes/provincias.csv'
  ivalues = 'notebooks/ivalue_entropia_personas_palabras.csv'
}else{
  cantidadesDataset = 'cantidadesDataset_test.csv'
  cantPorProv = 'contrastes/provincias_test.csv'
  ivalues = 'notebooks/ivalue_entropia_personas_palabras_test.csv'
}


cant <- read.csv(cantidadesDataset,row.names = 1,header = TRUE)

dfcantPalabrasEnProvincia <- read.csv(cantPorProv,row.names = 1)
df <- read.csv(ivalues)
colnames(df)[1] <- 'palabra'
cantPalabrasTotalesEnRegion <- function(provincias){
  sum(cant[provincias,]$cantTotal)
}

cantPalabrasWEnRegion <- function(palabra,provincias){
  provs <- paste(provincias, "Palabras", sep="")
  sum(dfcantPalabrasEnProvincia[palabra,provs])
}

cantPalabraWEnArgentina <- function(palabra){
  dfcantPalabrasEnProvincia[palabra,'cantPalabra']
}

palabrasEnArgentina = sum(cant$cantTotal)#192348167

pvalor <- function(palabra,totalEnRegion,wEnRegion){
  M = palabrasEnArgentina   # Cantidad de palabras en toda la Argentina 
  wEnArg = cantPalabraWEnArgentina(palabra) # Cantidad de palabras w en toda la Argentina 
  N = totalEnRegion    #cantPalabrasTotalesEnRegion(region) # Cantidad de palabras en la region
  h0 = wEnRegion#cantPalabrasWEnRegion(palabradf2,region)
  resto = palabrasEnArgentina-wEnArg
  #cat(h0,wEnArg,resto,palabrasEnArgentina-h0,N,'\n')
  cat(palabra,'\n')
  cat('\t','m es ',wEnArg,'\n')
  cat('\t','x es ',h0-1,'\n')
  cat('\t','n es ',resto,'\n')
  cat('\t','k-x es ',N-(h0-1),'\n')
  cat('\t','m+n es ',wEnArg+resto,'\n')
  cat('\t','k es ',N,'\n')
  
  cat('(q=',h0-1,',m =',wEnArg,',n=',resto,',k=',N,',lower.tail = FALSE,log.p = TRUE)\n')
  phyper(q=h0-1,m = wEnArg,n=resto,k=N,lower.tail = FALSE,log.p = TRUE)
}
# tenemos 175 millones de palabras, las cuales 7 millones son la palabra que.
# agarrp 142 millones de palabras (82% aprox) y obtengo 
# leo las primeras 5000 lineas del listado
def = read.csv('definitivo.csv')[1:4999,]
colnames(def)[1]<- 'palabra'
#x = def[def$Palabra.Candidata ==1,'palabra']
#x = x[1:10]   # Sacar esta línea para testear sobre todas las palabras candidatas
x = c('hola','que','de','cuando','la','el') 
df2 = df[is.element(df$palabra,x),]
df2$pvalorLog = apply(X = df2[,c('palabra', 'cantPalabrasTotalesEnRegion','cantPalabrasWEnRegion')],MARGIN =  1, FUN = function(x) { pvalor(x[1],as.numeric(x[2]),as.numeric(x[3]))} )
df2$pvalor = exp(df2$pvalorLog)

pv=df2[with(df2, order(pvalorLog)), c("palabra",'pvalor',"pvalorLog")]
pv$BH = p.adjust(pv$pvalor,method = 'BH')

#q= 6228544;m = 7457301; n= 167605080; k= 143850506
#p = m / (m+n)
#media = k* p
#varza = k * p *(1-p)  * (m+n-k)/(m+n-1)
#sd = sqrt(varza)

plot(x =seq(6000000,6339999,50),y= phyper(q=seq(6000000,6339999,50),m = 7457301, n= 167605080, k= 143850506,lower.tail = FALSE))

# el siguiente plot es con las cantidades de la palabra que
plot(x = seq(0.1,0.9,0.1),y=qhyper(p=seq(0.1,0.9,0.1),m = 7457301, n= 167605080, k= 143850506,lower.tail = FALSE))