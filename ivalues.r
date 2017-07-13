
cant <- read.csv('cantidadesDataset.csv',row.names = 1)
dfcantPalabrasEnProvincia <- read.csv("contrastes/provincias.csv",row.names = 1)
df <- read.csv('notebooks/ivalue_entropia_personas_palabras_resumida.csv',row.names(1))
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


palabrasEnArgentina = 192348167
pvalor <- function(palabra,totalEnRegion,wEnRegion){
  M = palabrasEnArgentina # Cantidad de palabras en toda la Argentina 
  wEnArg = cantPalabraWEnArgentina(palabra) # Cantidad de palabras w en toda la Argentina 
  N = totalEnRegion#cantPalabrasTotalesEnRegion(region) # Cantidad de palabras en la region
  
  h0 = wEnRegion#cantPalabrasWEnRegion(palabra,region)
  resto = palabrasEnArgentina-wEnArg
  phyper(q=h0,m = wEnArg,n=resto,k=N,lower.tail = FALSE)
}

apply(X = df[,c('palabra', 'cantPalabrasTotalesEnRegion','cantPalabrasWEnRegion')],MARGIN =  1, FUN = function(x) { pvalor(x[1],as.numeric(x[2]),as.numeric(x[3]))} )