
cant <- read.csv('cantidadesDataset_test.csv',row.names = 1,header = TRUE)

dfcantPalabrasEnProvincia <- read.csv("contrastes/provincias_test.csv",row.names = 1)
df <- read.csv('notebooks/ivalue_entropia_personas_palabras_test.csv')
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
  phyper(q=h0-1,m = wEnArg,n=resto,k=N,lower.tail = FALSE,log.p = TRUE)
}

def = read.csv('definitivo.csv')
colnames(def)[1]<- 'palabra'
x = def[def$Palabra.Candidata ==1,'palabra']
x = x[1:10]   # Sacar esta línea para testear sobre todas las palabras candidatas
df2 = df[is.element(df$palabra,x),]
df2$pvalorLog = apply(X = df2[,c('palabra', 'cantPalabrasTotalesEnRegion','cantPalabrasWEnRegion')],MARGIN =  1, FUN = function(x) { pvalor(x[1],as.numeric(x[2]),as.numeric(x[3]))} )
df2$pvalor = exp(df2$pvalorLog)

pv=df2[with(df2, order(pvalorLog)), c("palabra",'pvalor',"pvalorLog")]
pv$BH = p.adjust(pv$pvalor,method = 'BH')