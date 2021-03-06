##Import Required packages

import numpy as np
import os,sys
import pandas as pd
import re



error = []
out_path = r'/mnt/nfs/scratch1/kajaltiwari/data/unstructured/emb_pickle/'
final_path = r'/mnt/nfs/scratch1/kajaltiwari/data/structured/'

for filename in os.listdir():
    #os.chdir(out_path)
    df = pd.DataFrame()
    if filename.endswith(".pkl"):

        df = pd.read_pickle(filename)
        df = df.sort_values(by='year')
        if len(df.index) > 2:
            # print(filename)
            # print(df['embeddings1a'])
            temp11 = temp17 = temp21 = temp27 = pd.DataFrame()

            temp11 = df['embeddings1a'].shift(1)
            temp17 = df['embeddings7'].shift(1)
            temp21 = df['embeddings1a'].shift(2)
            temp27 = df['embeddings7'].shift(2)
            df['t-1embedding1a'] = temp11
            df['t-1embedding7b'] = temp17
            df['t-2embedding1a'] = temp21
            df['t-2embedding7b'] = temp27
            df.dropna(subset=["t-2embedding1a", 't-1embedding1a', 't-2embedding7b', 't-1embedding7b'], inplace=True)
            #os.chdir(final_path)
            #print(df)
            df.to_pickle(final_path+filename)

