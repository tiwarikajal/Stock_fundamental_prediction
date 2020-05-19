import pandas as pd
import os,sys
import re
import torch

inp_path = r'/home/tiwarikajal/embeddingdata'
out_path = r'/home/tiwarikajal/data/'
error = []
df = pd.DataFrame(columns=['year', 'Company', 'embeddings1a', 'embeddings7'])
df['embeddings1a'] = df['embeddings1a'].astype(object)
df['embeddings7'] = df['embeddings7'].astype(object)

for filename in os.listdir():
    if filename.endswith(".pt"):
        try:
            filename1 = re.split('[_ .]', filename)
            embedding1 = torch.load(filename)['item1a'].cpu().data.numpy()
            embedding2 = torch.load(filename)['item7'].cpu().data.numpy()

            if os.path.exists(out_path + filename1[0] + '.pkl'):
                df = pd.read_pickle(out_path + filename1[0] + '.pkl')
                df = df.append(pd.Series([filename1[1], filename1[0], embedding1[0], embedding2[0]], index=df.columns),
                               ignore_index=True)
                df.to_pickle(out_path + filename1[0] + '.pkl')
                df = pd.DataFrame(columns=['year', 'Company', 'embeddings1a', 'embeddings7'])
            else:
                df = df.append(pd.Series([filename1[1], filename1[0], embedding1[0], embedding2[0]], index=df.columns),
                               ignore_index=True)
                df.to_pickle(out_path + filename1[0] + '.pkl')
                df = pd.DataFrame(columns=['year', 'Company', 'embeddings1a', 'embeddings7'])
        except:
            error.append(filename)
            f = open("Errorlog.txt", "w")
            f.write(error)
            f.close()

