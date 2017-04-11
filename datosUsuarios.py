# coding: utf-8

import json
import pandas as pd
from pandas import DataFrame, Series
from apps import *
from datetime import timedelta
import csv



if __name__ == "__main__":
    

    for prov in argentina:
        i = 0
        paths = ['tweetsFinal/pares/']
        with open('csv/{0}.csv'.format(prov),'a') as fi:
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
        df =  pd.read_csv('csv/{0}.csv'.format(prov),encoding='utf-8', parse_dates=['tweet_created_at','created_at'], date_parser=dateparse,delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #pd.read_csv('csv/'+prov + '.csv',delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        df['tweet_created_at'] = pd.to_datetime(df['tweet_created_at'])
        df = df.sort_values(by='created_at')
        users = df[['user_id','created_at']].drop_duplicates('user_id')
        #print users.shape
        tot = users.shape[0]
        half = users.shape[0]/2
        users1 = users.iloc[0:half,:] 
        users2 = users.iloc[half:tot,:]
        #users1 = users.sample(frac=0.5)
        #users2=users.drop(users1.index)
        #print users1.shape, users2.shape
        train = df[df['user_id'].isin(users1['user_id'])].copy()    
        test = df[df['user_id'].isin(users2['user_id'])].copy()
        #print train.shape[0],test.shape[0], train.shape[0]+test.shape[0],df.shape[0]

        train.text.replace(regex=True,inplace=True,to_replace=['\r','\n'],value=r'')
        test.text.replace(regex=True,inplace=True,to_replace=['\r','\n'],value=r'')
        

        dmin1 = train['tweet_created_at'].min()
        dmax1 = train['tweet_created_at'].max()

        dmin2 = test['tweet_created_at'].min()
        dmax2 = test['tweet_created_at'].max()

        #t1 = train.shape[0]
        #t2 = test.shape[0]
        #print dmin1,dmax1,dmin2,dmax2
        #print t1,t2
        cant = train.shape[0]
        mitad = cant/2
        mintemp = min(dmin1,dmin2)
        maxtemp = max(dmax1,dmax2)
        dmin = mintemp
        dmax = maxtemp
        delta = (maxtemp - mintemp) /2
        print delta.days
        centro = mintemp+timedelta(seconds = delta.total_seconds())
        #print centro
        in_range_df1 = train[(train['tweet_created_at'] > dmin) & (train['tweet_created_at'] <= centro)]
        in_range_df2 = test[(test['tweet_created_at'] > centro) & (test['tweet_created_at'] <= dmax)]

        while abs(in_range_df1.shape[0] - in_range_df2.shape[0]) > 10 and delta.total_seconds() > 3600:
            in_range_df1 = train[(train['tweet_created_at'] > dmin) & (train['tweet_created_at'] <= centro)]
            in_range_df2 = test[(test['tweet_created_at'] > centro) & (test['tweet_created_at'] <= dmax)]

            if in_range_df1.shape[0] < in_range_df2.shape[0]:
                    mintemp = centro + timedelta(days = 1)
                    delta = (maxtemp - mintemp) /2
                    #print delta.days,'mas'
                    centro = centro + timedelta(seconds = delta.total_seconds())
                   
            elif in_range_df1.shape[0] > in_range_df2.shape[0]:
                    maxtemp = centro - timedelta(days = 1)
                    delta = (maxtemp - mintemp) /2
                    #print delta.days,'menos'
                    centro = centro - timedelta(seconds = delta.total_seconds())
            print centro, in_range_df1.shape[0], in_range_df2.shape[0],delta.seconds    

        #print prov,centro,in_range_df1.shape[0], in_range_df2.shape[0]

       
        with open('csv/train_{0}.csv'.format(prov), 'wb') as trainAllCols, \
             open('train/train_{0}.csv'.format(prov), 'wb') as trainMin:
              
            train_df = in_range_df1.loc[:,['tweet_id','user_id','text']] 
            train_df.to_csv(trainMin,encoding='utf-8', header=None, index=False,quotechar='|', quoting=csv.QUOTE_MINIMAL)
            in_range_df1.to_csv(trainAllCols,encoding='utf-8', index=False,quotechar='|', quoting=csv.QUOTE_MINIMAL)
        with open('csv/test_{0}.csv'.format(prov), 'wb') as testAllCols, \
             open('test/test_{0}.csv'.format(prov), 'wb') as testMin:
            test_df = in_range_df2.loc[:,['tweet_id','user_id','text']] 
            test_df.to_csv(testMin,encoding='utf-8', header=None, index=False,quotechar='|', quoting=csv.QUOTE_MINIMAL)
            in_range_df2.to_csv(testAllCols,encoding='utf-8', index=False,quotechar='|', quoting=csv.QUOTE_MINIMAL)
    