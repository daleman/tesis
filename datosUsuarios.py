# coding: utf-8

import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame, Series
import seaborn as sns 
from apps import *
from datetime import timedelta
import csv
from datetime import timedelta
import pickle 



if __name__ == "__main__":
    

    for prov in argentina:
        i = 0
        paths = ['tweetsFinal/pares/','tweetsFinal/impares/']
        with open('csv/' + prov + '.csv','a') as fi:
            csvwriter = csv.writer(fi, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(('tweet_created_at','text','tweet_id','user_id','screen_name', 'friends', 'followers','statuses_count','favorites','geo_enabled','created_at','location'))
            for path in paths:
                file_path = path + prov + '_tweets.json'
                with open(file_path) as f:
                    for line in f:
                        tweet = json.loads(line)
                        csvwriter.writerow((tweet['created_at'].encode('utf-8'),tweet['text'].encode('utf-8'),tweet['id'],tweet['user']['id'],tweet['user']['screen_name'].encode('utf-8'),tweet['user']['friends_count'],tweet['user']['followers_count'],tweet['user']['statuses_count'],tweet['user']['favourites_count'],tweet['user']['geo_enabled'],tweet['user']['created_at'].encode('utf-8'),tweet['user']['location'].encode('utf-8')))
                        i +=1
                

        print prov
        dateparse = lambda x: pd.datetime.strptime(x, '%a %b %d %H:%M:%S +0000 %Y')
        df =  pd.read_csv('csv/'+prov + '.csv',encoding='utf-8', parse_dates=['tweet_created_at','created_at'], date_parser=dateparse,delimiter=',',quotechar='|')
        #pd.read_csv('csv/'+prov + '.csv',delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        df['tweet_created_at'] = pd.to_datetime(df['tweet_created_at'])
        users = df['user_id'].drop_duplicates()
        #print users.shape
        users1 = users.sample(frac=0.5)
        users2=users.drop(users1.index)
        #print users1.shape, users2.shape
        train = df[df['user_id'].isin(users1)]
        test = df[df['user_id'].isin(users2)]
        #print train.shape[0],test.shape[0], train.shape[0]+test.shape[0],df.shape[0]

        dmin1 = train['tweet_created_at'].min()
        dmax1 = train['tweet_created_at'].max()

        dmin2 = test['tweet_created_at'].min()
        dmax2 = test['tweet_created_at'].max()

        t1 = train.shape[0]
        t2 = test.shape[0]
        #print dmin1,dmax1,dmin2,dmax2
        #print t1,t2
        cant = train.shape[0]
        mitad = cant/2
        mintemp = min(dmin1,dmin2)
        maxtemp = max(dmax1,dmax2)
        dmin = mintemp
        dmax = maxtemp
        delta = (maxtemp - mintemp) /2
        #print delta.days
        centro = mintemp+timedelta(delta.days)
        #print centro
        in_range_df1 = train[(train['tweet_created_at'] > dmin) & (train['tweet_created_at'] <= centro)]
        in_range_df2 = test[(test['tweet_created_at'] > centro) & (test['tweet_created_at'] <= dmax)]

        while abs(in_range_df1.shape[0] - in_range_df2.shape[0]) > 10 and delta.days > 1:
            in_range_df1 = train[(train['tweet_created_at'] > dmin) & (train['tweet_created_at'] <= centro)]
            in_range_df2 = test[(test['tweet_created_at'] > centro) & (test['tweet_created_at'] <= dmax)]

            if in_range_df1.shape[0] < in_range_df2.shape[0]:
                    mintemp = centro + timedelta(days = 1)
                    delta = (maxtemp - mintemp) /2
                    #print delta.days,'mas'
                    centro = centro + timedelta(days = delta.days)
                   
            elif in_range_df1.shape[0] > in_range_df2.shape[0]:
                    maxtemp = centro - timedelta(days = 1)
                    delta = (maxtemp - mintemp) /2
                    #print delta.days,'menos'
                    centro = centro - timedelta(days = delta.days)
            #print centro, in_range_df1.shape[0], in_range_df2.shape[0],delta.days    

        print prov,centro,in_range_df1.shape[0], in_range_df2.shape[0]

       
        with open('csv/train_' + prov + '.csv', 'wb') as output:
            pickle.dump(in_range_df1, output)

        with open('csv/test_' + prov + '.csv', 'wb') as output:
            pickle.dump(in_range_df2, output)
       
        #in_range_df1.to_csv('csv/train_' + prov + '.csv',encoding='utf-8', index=False,delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #in_range_df2.to_csv('csv/test_'  + prov + '.csv',encoding='utf-8', index=False,delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)