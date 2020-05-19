
import numpy as np
import os,sys
import pandas as pd
import re

in_path=r'/mnt/nfs/scratch1/nagarwal/data_merge/sentiment_score_merge/folder2/'
out_path=r'/mnt/nfs/scratch1/nagarwal/data_merge/sentiment_score_merge/folder3/'

#os.chdir(final_path)
df_struc = df_emb = pd.DataFrame()

for filename in os.listdir(in_path):
    if filename.endswith('.csv') == True:

        file_temp = filename.split('.')

        for filename1 in os.listdir(in_path):
            if filename1.endswith('.pkl') == True and filename1.endswith('_final.pkl') == False:
                # print(filename,filename1)
                temp = filename1.split('.')
                if temp[0] == file_temp[0]:

                    df_struc = pd.read_csv(in_path + filename)
                    df_emb = pd.read_pickle(in_path+filename1)
                    df_emb['FundamentalAtT'] = 'StructuredDataNotFound'
                    for index, row in df_emb.iterrows():
                        for i, r in df_struc.iterrows():
                            if str(r['year']) == row['year']:
                                df_emb.loc[index, 'FundamentalAtT'] = r['Revenue']
                                print(df_emb)
                    df_emb.to_pickle(out_path+temp[0] + '_final.pkl')
