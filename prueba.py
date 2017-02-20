# coding: utf-8
import re
from nltk import word_tokenize
import datetime

import os
from pygeocoder import Geocoder
from math import  *
import scipy.stats as stat
from scipy.stats import norm
import statsmodels.api as sm
import statsmodels.stats as sta
from apps import *
import nltk
from nltk import word_tokenize

def do_geocode(address):
    try:
        return geopy.geocode(address)
    except :
        return do_geocode(address)

def geocode(address):
    g = geocoders.GoogleV3()
    place, (lat, lng) = g.geocode(address)
    print '%s: %.5f, %.5f' % (place, lat, lng)
    return place, lat, lng

    #http://www.darrinward.com/lat-long/?id=2563726

def ztest(x1,x2,n1,n2):
    p1 = x1/n1
    p2 = x2/n2
    p = (x1 + x2) / (n1 + n2)
    print p
    den = sqrt(p*(1.0-p)*((1/n1)+(1/n2)))
    print p, 1-p, 1/n1,1/n2
    print den
    z = (p1-p2) / den 
    return z 

from scipy import stats
#Studnt, n=999, p<0.05, 2-tail
#equivalent to Excel TINV(0.05,999)

def twoSampZ(X1, X2, mudiff, sd1, sd2, n1, n2):
    from numpy import sqrt, abs, round
    from scipy.stats import norm
    pooledSE = sqrt(sd1**2/n1 + sd2**2/n2)
    z = ((X1 - X2) - mudiff)/pooledSE
    pval = 2*(1 - norm.cdf(abs(z)))
    return round(z, 3), round(pval, 4)

def pvalor(z):
    import scipy.stats as st
    nz = z 
    if z > 0:
        nz = -z
    return 2*st.norm.cdf(nz)

def tokenize(texto):
    #import ipdb; ipdb.set_trace()
    #print m
    texto = re.sub('@[\wáéíóú]*', '', texto)
    texto = re.sub('#[\wáéíóú]*', '', texto)
    texto = re.sub(r'http\S+', '', texto)
    texto = re.findall('[^\W\d]+', texto, re.UNICODE)
    texto =' '.join(texto)
    tokens =  word_tokenize(texto)
    return tokens

if __name__ == "__main__":
    #print stats.t.ppf(1-0.025, 999)
    
    #print 2*st.norm.cdf(-8.99)
    word_tokenizer=nltk.data.load('tokenizers/punkt/spanish.pickle')
    # texto = 'hola @youtube como #baila @lala httpsasdasd hola',
    # print texto
    # texto = re.sub('@[\w]*', '', texto)
    # print texto
    # texto = re.sub('#[\w]*', '', texto)
    # print texto
    # texto = re.sub(r'http\S+', '', texto)
    # print word_tokenize(texto)
    # print datetime.datetime.now()
    # ci = ['Rio de Janeiro','Salvador','Belo Horizonte','Fortaleza','BRASILIA','Curitiba','Recife','Porto Alegre','Manaus','Belém','Guarulhos','Goiânia','Campinas','Sao Gonçalo','Nova Iguaçu','Sao Luís','Maceió','Duque de Caxias','Sao Bernardo do Campo','Teresina','Natal','Osasco','Campo Grande','Santo André','Joao Pessoa','Jaboatao dos Guarapes','Contagem','Sao José dos Campos','Uberlândia','Feira de Santana','Ribeirao Prêto','Sorocaba','Niterói','Cuiabá','Juiz de Fora','Aracaju','Sao Joao de Meriti','Londrina','Joinville','Belford Roxo','Ananindeua','Santos','Campos dos Goytacazes','Mauá','Carapicuíba','Sao José do Rio Prêto','Caxias do Sul','Olinda','Campina Grande','Moji das Cruzes','Aparecida de Goiania','Diadema','Vila Velha','Piracicaba','Cariacica','Bauru','Pelotas','Betim','Porto Velho','Serra','Franca','Canoas','Jundiaí','Maringá','Montes Claros','Sao Vicente','Anápolis','Florianópolis','Itaquaquecetuba','Petrópolis','Ponta Grossa','Vitória','Rio Branco','Foz do Iguaçu','Macapá','Ilhéus','Vitória da Conquista','Uberaba','Paulista','Limeira','Blumenou','Caruaru','Caucaia','Nôvo Hamburgo','Ribeirao das Neves','Cascavel','Volta Redonda','Santa Maria','Santarém','Guarujá','Taubaté','Governador Valadares','Embu','Gravatai','Imperatriz','Varzea Grande','Barueri','Mossoró','Petrolina']
    # #for c in ci:
    # #    result = Geocoder.geocode(c+',brasil')
    # #    print str(result.coordinates[0]) + ',' + str(result.coordinates[1])
    # #t,pvalue = sta.weightstats.ztest(x1=[2,2,2,3],x2=[2,2,3,2])
    # #print t
    # #print pvalue
    # #z = ztest(351.0,41.0,605.0,195.0)
    # #print z
    # #print pvalor(z)
    # from math import erf,sqrt
    # z = 8.99
    # p=0.5*(1.0+erf(z/sqrt(2.0)))
    # print 2*(1-p)
    #tok = tokenize('#Fútbol pibe fútbol')
    #for w in tok:
    #    print w
    ci = ['Arica ,Chile','Putre ,Chile','Iquique ,Chile','Pozo Almonte ,Chile','Tocopilla   ,Chile',
'Calama  ,Chile','Antofagasta   ,Chile','Chañaral ,Chile','Copiapó   ,Chile','Vallenar ,Chile',
'Coquimbo , La Serena  ,Chile','Ovalle  ,Chile','Illapel ,Chile','La Ligua ,Chile','Los Andes   ,Chile',
'San Felipe  ,Chile','Quillota ,Chile','Valparaíso ,Chile','San Antonio ,Chile','Hanga Roa ,Chile','Quilpué ,Chile','Colina  ,Chile',
'Santiago de Chile  ,Chile','Puente Alto ,Chile','San Bernardo ,Chile','Melipilla   ,Chile','Talagante   ,Chile','Rancagua  ,Chile','San Fernando ,Chile','Pichilemu   ,Chile','Curicó  ,Chile','Talca  ,Chile','Linares ,Chile','Cauquenes   ,Chile','Chillán ,Chile','Los Ángeles ,Chile','Concepción    ,Chile','Lebu ,Chile','Angol   ,Chile','Temuco    ,Chile','Valdivia  ,Chile','La Unión ,Chile','Osorno  ,Chile','Puerto Montt  ,Chile','Castro  ,Chile','Chaitén ,Chile',
'Coyhaique  ,Chile','Puerto Aysén ,Chile','Chile Chico ,Chile','ochrane ,Chile','Puerto Natales  ,Chile','Punta Arenas  ,Chile','Porvenir ,Chile','Puerto Williams ,Chile']
   
ciBolivia = [
'Cercado Beni',
'Antonio Vaca Díez',
'General José Ballivián Segurola',
'Yacuma',
'Moxos',
'Marbán',
'Mamoré',
'Iténez',
'Oropeza',
'Juana Azurduy de Padilla',
'Jaime Zudáñez',
'Tomina',
'Hernando Siles',
'Yamparáez',
'Nor Cinti',
'Sud Cinti',
'Belisario Boeto',
'Luis Calvo',
'Arani',
'Esteban Arce',
'Arque',
'Ayopaya',
'Campero',
'Capinota',
'Cercado',
'Carrasco',
'Chapare',
'Germán Jordán',
'Mizque',
'Punata',
'Quillacollo',
'Tapacarí',
'Bolívar',
'Tiraque',
'Aroma',
'Bautista Saavedra',
'Abel Iturralde',
'Caranavi',
'Eliodoro Camacho',
'Franz Tamayo',
'Gualberto Villaroel',
'Ingavi',
'Inquisivi',
'General José Manuel Pando',
'Larecaja',
'Loayza',
'Los Andes',
'Manco Kapac',
'Muñecas',
'Nor Yungas',
'Omasuyos',
'Pacajes',
'Pedro Domingo Murillo',
'Sud Yungas',
'Sabaya',
'Carangas',
'Cercado',
'Eduardo Avaroa',
'Ladislao Cabrera',
'Litoral',
'Mejillones',
'Nor Carangas',
'Pantaleón Dalence',
'Poopó',
'Sajama',
'San Pedro de Totora',
'Saucarí',
'Sebastián Pagador',
'Sud Carangas ',
'Tomas Barrón',
'Abuná',
'Federico Román',
'Madre de Dios',
'Manuripi',
'Nicolás Suárez',
'Alonzo de Ibáñez',
'Antonio Quijarro',
'Bernardino Bilbao',
'Charcas',
'Chayanta',
'Cornelio Saavedra',
'Daniel Saavedra',
'Enrique Baldivieso',
'José María Linares',
'Modesto Omiste',
'Nor Chichas',
'Nor Lípez',
'Rafael Bustillo',
'Sud Chichas',
'Sud Lipez',
'Tomás Frías',
'Andrés Ibáñez',
'Ignacio Warnes',
'José Miguel de Velasco',
'Ichilo',
'Chiquitos',
'Sara',
'Cordillera',
'Vallegrande',
'Florida',
'Santistevan',
'Ñuflo de Chávez',
'Ángel Sandoval',
'Caballero',
'Germán Busch',
'Guarayos',
'Aniceto Arce',
'Burdet OConnor',
'Cercado Tarija',
'Eustaquio Méndez',
'Gran Chaco',
'José María Avilés']
for c in ciBolivia:
    try:
        result = Geocoder.geocode(c + ' bolivia')
        print str(result.coordinates[0]) + ',' + str(result.coordinates[1])
    except:
        #print c, 'sin coordenadas'
        continue