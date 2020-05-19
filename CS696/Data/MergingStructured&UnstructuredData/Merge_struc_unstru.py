
import numpy as np
import os,sys
import pandas as pd
import re

#out_path=r'/content/drive/My Drive/696 Dataset/scratch1/data_netincome/emb_pickle/'
final_path=r'/mnt/nfs/scratch1/kajaltiwari/data/structured/'

#os.chdir(final_path)
df_struc = df_emb = pd.DataFrame()

for filename in os.listdir():
    if filename.endswith('.csv') == True:

        file_temp = filename.split('.')

        for filename1 in os.listdir():
            if filename1.endswith('.pkl') == True and filename1.endswith('_final.pkl') == False:
                # print(filename,filename1)
                temp = filename1.split('.')
                if temp[0] == file_temp[0]:

                    df_struc = pd.read_csv(filename)
                    df_emb = pd.read_pickle(filename1)
                    df_emb['FundamentalAtT'] = 'StructuredDataNotFound'
                    for index, row in df_emb.iterrows():
                        for i, r in df_struc.iterrows():
                            if str(r['year']) == row['year']:
                                df_emb.loc[index, 'FundamentalAtT'] = r['NetIncomeLoss']
                                print(df_emb)
                    df_emb.to_pickle(temp[0] + '_final.pkl')

final = pd.DataFrame()
for filename in os.listdir():
    temp = pd.DataFrame()
    if filename.endswith('_final.pkl'):
        temp = pd.read_pickle(filename)
        final = pd.concat([final, temp])
final.to_pickle('Augmented_Dataset.pkl')