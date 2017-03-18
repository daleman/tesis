# coding: utf-8
from apps import *
import pickle
for prov in argentina:
    with open('csv/train_' + prov+ '.csv', 'rb') as fi:
        df= pickle.load(fi)
    df['text'] = df['text'].str.replace('\n', '')
    indexed_df = df[['tweet_id','user_id','text']]
    indexed_df.to_csv('train/train_' + prov +'.csv',encoding='utf-8', header=None, index=False)
    num_lines = sum(1 for line in open('train/train_'+prov+'.csv'))
    print 'train',prov, df['text'].shape,num_lines
    with open('csv/test_' + prov+ '.csv', 'rb') as fi:
        df= pickle.load(fi)
    df['text'] = df['text'].str.replace('\n', '')
    indexed_df = df[['tweet_id','user_id','text']]
    indexed_df = df.set_index('tweet_id')
    indexed_df.to_csv('test/test_' + prov +'.csv',encoding='utf-8', header=None, index=False)
    num_lines = sum(1 for line in open('test/test_'+prov+'.csv'))
    print 'test',prov, df['text'].shape,num_lines
    