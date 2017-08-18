library(tidyverse)
library(ggmap)
library(DT)
library(knitr)
library(rgdal)
library(scales)
library(splitstackshape)

hacerMapa = function(provODep,puntos){
  setwd("~/")
  
  if (provODep == 'provincias'){
    shape = readOGR('Downloads/dep/',layer = 'departamentos')
    regiones = fortify(shape,region = 'PROVINCIA')
  }else{
    shape = readOGR('Downloads/dep/',layer = 'departamentos')
    regiones = fortify(shape,region = 'CABECERA' )
  }
  
  tweets = read.csv('tesis/notebooks/locations2_geocoded.csv',header = TRUE)
  
  #Para ver todos los tweets con coordenadas descomentar la siguiente linea y comentar la linea de expandRows
  #tweets = read.csv('tesis/latex/src/resultados/cooords2.csv',header = TRUE)
  tweets = expandRows(tweets, "total")
  coords = tweets[c("long", "lat")]
  coords = na.omit(coords)
  #View(coords)
  sp = SpatialPoints(coords)
  
  proj4string(sp) <- "+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0,0,0"
  by_tract = over(sp,shape)
  if (provODep == 'provincias'){
    by_tract <- by_tract %>%
    group_by(PROVINCIA) %>%
    summarise(total=n())
  }else{
    by_tract <- by_tract %>%
    group_by(CABECERA) %>%
    summarise(total=n())
    
  }
  colnames(by_tract) <- c("id", "total")
  
  by_tract$id <- as.character(by_tract$id)
  by_tract = na.omit(by_tract)
  #by_tract[by_tract$id == 'BUENOS AIRES',]$total = by_tract[by_tract$id == 'BUENOS AIRES',]$total + by_tract[by_tract$id == 'CAPITAL FEDERAL',]$total
  #by_tract = by_tract[!by_tract$id == 'CAPITAL FEDERAL',]
  
  total_map <- left_join(regiones, by_tract)
  View(by_tract)
  mapa <- ggplot() 
  
  mapa <- mapa +  geom_polygon(data = total_map, aes(x=long, y=lat, group=group, fill=total), color = "black", size=0.2)
  #mapa <- mapa +  geom_polygon(data = provincias, aes(x=long, y=lat, group=group,fill=NA), color='black',fill=NA,  size=0.2) 
  mapa <- mapa +  coord_map("polyconic", xlim=c(-75, -52), ylim=c(-55, -20)) 
  mapa <- mapa + scale_fill_distiller(type="seq", trans="reverse", palette = "Reds", breaks=pretty_breaks(n=10)) 
  fPuntos = ''
  if (puntos){
    mapa <- mapa +  geom_point(data=coords, aes(x=long, y=lat),size= 0.2)
    fPuntos = 'ConPuntos'
  }
  mapa <- mapa + theme(legend.title=element_blank())
  
  mapa <- mapa + theme_nothing(legend=TRUE) 
  #print(mapa)
  ggsave(filename=paste("mapa",provODep,fPuntos,".pdf",sep = ''), plot=mapa)
}

hacerMapa('provincias', FALSE)
hacerMapa('departamentos', FALSE)
hacerMapa('provincias', TRUE)


