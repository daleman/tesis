# coding: utf-8
from apps import *
import pickle
import csv

for prov in argentina:
    with open('csv/train_' + prov+ '.csv', 'rb') as fi:
        df= pickle.load(fi)
    indexed_df = df.loc[:,['tweet_id','user_id','text']]
    indexed_df['text'].replace(regex=True,inplace=True,to_replace=['\r','\n'],value=r'')
    indexed_df.to_csv('train/train_' + prov +'.csv',encoding='utf-8', header=None, index=False,delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    num_lines = sum(1 for line in open('train/train_'+prov+'.csv'))
    print 'train',prov, df['text'].shape,num_lines
    with open('csv/test_' + prov+ '.csv', 'rb') as fi:
        df= pickle.load(fi)
    indexed_df = df.loc[:,['tweet_id','user_id','text']]
    indexed_df['text'].replace(regex=True,inplace=True,to_replace=['\r','\n'],value=r'')
    indexed_df.to_csv('test/test_' + prov +'.csv',encoding='utf-8', header=None, index=False,delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    num_lines = sum(1 for line in open('test/test_'+prov+'.csv'))
    print 'test',prov, df['text'].shape,num_lines
    