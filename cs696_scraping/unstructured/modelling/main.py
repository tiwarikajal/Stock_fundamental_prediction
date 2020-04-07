import torch
from model import UnStructuredModel
import pandas as pd
from os import listdir, mkdir
from os.path import isfile, join, isdir
files_path = "../../../"

files = ["yoy1.csv", "yoy2.csv", "yoy3.csv", "yoy4.csv", "yoy5.csv", "yoy6.csv", "yoy7.csv", "yoy8.csv", "yoy9.csv", "yoy10.csv","yoy11.csv"]


# files = ["yoy13.csv", "yoy12.csv"]
sections = ["Ticker", "Company Name", "Industry", "Top 100", "item1a", "item2"]
param_sections = ["item1a", "item2"]
max_length = 500
stride = 250
model_name = 'bert-base-uncased'
embeddingsPath = "embeddingdata" + '_'+ str(max_length) + '_' + str(stride)+ str(model_name)
embeddingsPath = join(files_path, embeddingsPath)
if not isdir(embeddingsPath):
    mkdir(embeddingsPath)

def main():
    unstructuredmodel = UnStructuredModel(model_name, max_length, stride)
    for file in files:
        df = pd.read_csv(files_path+file) 
        for i in range(len(df)):
            row = df.iloc[i]
            embeddingDict = {}
            embeddingFile = join(embeddingsPath, row["Ticker"] + ".pt")
            if isfile(embeddingFile):
                embeddingDict = torch.load(embeddingFile)
            for section in sections:
                if section not in param_sections and section in row.keys():
                    embeddingDict[section] = row[section]
            for section in param_sections:
                if section in row.keys() and len(row[section])>100:
                    if section not in embeddingDict.keys():
                        embeddingDict[section] = {}
                    embeddingDict[section][int(row["Year"]) + 2000] = unstructuredmodel.getEmbedding(text=row[section],if_pool=False)
                        
            torch.save(embeddingDict,embeddingFile)     


if __name__== "__main__":
    main()