# coding: utf-8
from apps import *
import pandas as pd
import csv

for prov in argentina:
    dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    with open('csv/train_{0}.csv'.format(prov), 'rb') as fi:
        #df= pickle.load(fi)
        df =  pd.read_csv(fi,encoding='utf-8', parse_dates=['tweet_created_at','created_at'], date_parser=dateparse,delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
       
    indexed_df = df.loc[:,['tweet_id','user_id','text']]
    indexed_df['text'].replace(regex=True,inplace=True,to_replace=['\r','\n'],value=r'')
    indexed_df.to_csv('train/train_{0}.csv'.format(prov),encoding='utf-8', header=None, index=False,delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    num_lines = sum(1 for line in open('train/train_{0}.csv'.format(prov)))
    print 'train',prov, df['text'].shape,num_lines
    with open('csv/test_{0}.csv'.format(prov), 'rb') as fi:
        df =  pd.read_csv(fi,encoding='utf-8', parse_dates=['tweet_created_at','created_at'], date_parser=dateparse,delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    indexed_df = df.loc[:,['tweet_id','user_id','text']]
    indexed_df['text'].replace(regex=True,inplace=True,to_replace=['\r','\n'],value=r'')
    indexed_df.to_csv('test/test_{0}.csv'.format(prov),encoding='utf-8', header=None, index=False,delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    num_lines = sum(1 for line in open('test/test_{0}.csv'.format(prov)))
    print 'test',prov, df['text'].shape,num_lines
    