import pandas as pd
import os,sys
import re
import torch
import json

#inp_path = r'/mnt/nfs/scratch1/nagarwal/CS696_Stock_fundamental_prediction/embeddingsdata_token_avg_max__500_250finroberta/'
inp_path = "/mnt/nfs/scratch1/nagarwal/CS696_Stock_fundamental_prediction/sentimentscore/"
out_path = r'/mnt/nfs/scratch1/nagarwal/data_merge/sentiment_score_merge/folder1/'
error = []
df = pd.DataFrame(columns=['year', 'Company', 'embeddings1a', 'embeddings7'])
#df['embeddings1a'] = df['embeddings1a'].astype(object)
#df['embeddings7'] = df['embeddings7'].astype(object)

for filename in os.listdir(inp_path):
    #filename = os.path.join(inp_path, filename)
    if filename.endswith(".json"):
        try:
            filename1 = re.split('[_ .]', filename)
            print(filename1)
            sentFile = open(os.path.join(inp_path + filename),"r")
            sentData = json.loads(sentFile.read())
            sentFile.close()
            embedding1 = sentData["item1a"]
            embedding2 = sentData["item7"]

            if os.path.exists(out_path + filename1[0] + '.pkl'):
                #os.chdir(out_path)
                df = pd.read_pickle(out_path + filename1[0] + '.pkl')
                df = df.append(pd.Series([filename1[1], filename1[0], embedding1, embedding2], index=df.columns),
                               ignore_index=True)
                df.to_pickle(out_path+filename1[0] + '.pkl')
                df = pd.DataFrame(columns=['year', 'Company', 'embeddings1a', 'embeddings7'])
            else:
                df = df.append(pd.Series([filename1[1], filename1[0], embedding1, embedding2], index=df.columns),
                               ignore_index=True)
                df.to_pickle(out_path + filename1[0] + '.pkl')
                df = pd.DataFrame(columns=['year', 'Company', 'embeddings1a', 'embeddings7'])
      
        except Exception as e:
            print("Error: {}".format(e))
            error.append(filename)
    #break 
f = open("Errorlog.txt", "w+")
f.write(str(error))
f.close()

