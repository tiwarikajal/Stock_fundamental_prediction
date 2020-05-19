import torch
import os
import pandas as pd

inp_path = "/mnt/nfs/scratch1/nagarwal/data_merge/temp2/folder3/"
out_path = "/mnt/nfs/scratch1/nagarwal/data_merge/temp2/"
#os.chdir(final_path)
final = pd.DataFrame()
for filename in os.listdir(inp_path):
    temp = pd.DataFrame()
    if filename.endswith('_final.pkl'):
        temp = pd.read_pickle(inp_path + filename)
        final = pd.concat([final, temp])
#final.drop( final[ final['FundamentalAtT'] == 'StructuredDataNotFound' ].index , inplace=True)
final.to_pickle(out_path+'Augmented_Dataset.pkl')
#Intermediate Dataset:
#final_df=pd.DataFrame(columns=['x','y'])
#final=pd.read_pickle('Augmented_Dataset.pkl')
#for i, r in final.iterrows():
    #temp=torch.stack([torch.tensor(r['t-1embedding1a']),torch.tensor(r['t-2embedding1a']),torch.tensor(r['t-1embedding7b']),torch.tensor(r['t-2embedding7b'])],0)
   # temp=temp.view(1,-1)
  #  final_df.loc[i,'x']=temp
 #   final_df.loc[i,'y']=r['FundamentalAtT']
  #print(final_df)
#final_df.to_pickle('Final_Dataset.pkl')
