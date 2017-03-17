# coding: utf-8
from apps import *
for prov in argentina:
    with open('csv/train_' + prov+ '.csv', 'rb') as fi:
        df= pickle.load(fi)
    df['text'] = df['text'].str.replace('\n', '')
    df['text'].to_csv('train/train_' + prov +'.txt',encoding='utf-8', header=None, index=False)
    num_lines = sum(1 for line in open('train/train_'+prov+'.txt'))
    print 'train',prov, df['text'].shape,num_lines
    with open('csv/test_' + prov+ '.csv', 'rb') as fi:
        df= pickle.load(fi)
    df['text'] = df['text'].str.replace('\n', '')
    df['text'].to_csv('test/test_' + prov +'.txt',encoding='utf-8', header=None, index=False)
    num_lines = sum(1 for line in open('test/test_'+prov+'.txt'))
    print 'test',prov, df['text'].shape,num_lines
    