import pandas as pd
import os,sys
import re
import torch

#inp_path = r'/mnt/nfs/scratch1/nagarwal/CS696_Stock_fundamental_prediction/embeddingsdata_token_avg_max__500_250finroberta/'
#inp_path = "/mnt/nfs/scratch1/nagarwal/CS696_Stock_fundamental_prediction/embeddingdata_max__500_250finroberta/"
inp_path = "/mnt/nfs/scratch1/nagarwal/CS696_Stock_fundamental_prediction/data_10K_3K/embeddingdata_max__500_250bert-base-uncased/"
out_path = r'/mnt/nfs/scratch1/nagarwal/data_merge/temp2/folder1/'
error = []
df = pd.DataFrame(columns=['year', 'Company', 'embeddings1a', 'embeddings7'])
df['embeddings1a'] = df['embeddings1a'].astype(object)
df['embeddings7'] = df['embeddings7'].astype(object)

for filename in os.listdir(inp_path):
    #filename = os.path.join(inp_path, filename)
    if filename.endswith(".pt"):
        try:
            filename1 = re.split('[_ .]', filename)
            print(filename1)
            embedding1 = torch.load(inp_path+filename)['item1a'].cpu().data.numpy()
            embedding2 = torch.load(inp_path+filename)['item7'].cpu().data.numpy()

            if os.path.exists(out_path + filename1[0] + '.pkl'):
                #os.chdir(out_path)
                df = pd.read_pickle(out_path + filename1[0] + '.pkl')
                df = df.append(pd.Series([filename1[1], filename1[0], embedding1[0], embedding2[0]], index=df.columns),
                               ignore_index=True)
                df.to_pickle(out_path+filename1[0] + '.pkl')
                df = pd.DataFrame(columns=['year', 'Company', 'embeddings1a', 'embeddings7'])
            else:
                df = df.append(pd.Series([filename1[1], filename1[0], embedding1[0], embedding2[0]], index=df.columns),
                               ignore_index=True)
                df.to_pickle(out_path + filename1[0] + '.pkl')
                df = pd.DataFrame(columns=['year', 'Company', 'embeddings1a', 'embeddings7'])

        except Exception as e:
            print("Error: {}".format(e))
            error.append(filename)
f = open("Errorlog.txt", "w+")
f.write(str(error))
f.close()

