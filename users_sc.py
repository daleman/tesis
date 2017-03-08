
# coding: utf-8

import os
from apps import * 
import datetime

import argparse
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("n_app", help="el numero de aplicacion con que empieza la busqueda",
                        type=int)
    parser.add_argument("mod_print", help="el numero de iteraciones por cada coordenada dentro del loop",
                        type=int)
    parser.add_argument("tot_tweets", help="el numero total de tweets por cada region/provincia",
                        type=int)
    parser.add_argument("pais", help="el pais donde se van a buscar los usuarios",
                        type=str)
 
    args = parser.parse_args()
    n_app = args.n_app
    mod_print = args.mod_print
    tot_tweets = args.tot_tweets
    pais = paises[args.pais.lower()]
    print pais
    
    start_tot = datetime.datetime.now()
    inc_app = int(250 / len(pais))
    for prov in pais.keys():
        start = datetime.datetime.now()
        comando = "python users.py " + str(n_app) + ' ' + str(mod_print) + ' ' + str(tot_tweets) + ' ' +   str(prov) + ' &'
        os.system(comando)
        n_app += inc_app  
        end = datetime.datetime.now()
        diff = (end - start)
        print pais[prov]['name'] , diff 

    end_tot = datetime.datetime.now()
    diff = (end_tot - start_tot)
    print args.pais , diff 
  