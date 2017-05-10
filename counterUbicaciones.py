import json
from apps import *
from collections import Counter
import csv
import operator
import numpy as np
import matplotlib.pyplot as plt
import pylab


locations = {}
c = {}

for prov in argentina:
    locations[prov] = []
    with open('./users/{0}_users.json'.format(prov),'r') as fi:
        for line in fi:
            tweet = json.loads(line)
            locations[prov].append(tweet['location'])
i=0
for prov in argentina:
    i+=1
    with open('./users/{0}_users.csv'.format(prov),'w') as fi:
        writer = csv.writer(fi, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
     
        c[prov] = Counter(locations[prov])
        mc = c[prov].most_common(30)
        #print prov, c[prov].most_common(10)
        labels, values = zip(*mc)

        indexes = np.arange(len(values))
        width = 1
        plt.figure(i)
        plt.bar(indexes,values)
        plt.xticks(indexes, labels,rotation=90)
        pylab.savefig('./users/{0}_users.png'.format(prov), bbox_inches='tight')
        for key, count in sorted(c[prov].iteritems(), key=operator.itemgetter(1),reverse=True):
            writer.writerow([key.encode('utf-8'),count])


