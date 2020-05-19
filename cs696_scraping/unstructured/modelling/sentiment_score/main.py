from finbert.finbert import predict
from pytorch_pretrained_bert.modeling import BertForSequenceClassification
#import argparse
import datetime
import os
import pandas as pd
import re
import json
#parser = argparse.ArgumentParser(description='Sentiment analyzer')

#parser.add_argument('-a', action="store_true", default=False)

#parser.add_argument('--text_path', type=str, help='Path to the text file.')
#parser.add_argument('--output_dir', type=str, help='Where to write the results')
#parser.add_argument('--model_path', type=str, help='Path to classifier model')
model_path = "/mnt/nfs/scratch1/nagarwal/sentiment_score/finBERT/models/classifier_model/finbert-sentiment"
inputpath = "/mnt/nfs/scratch1/nagarwal/CS696_Stock_fundamental_prediction/data_10K_3K/"
outputpath = "/mnt/nfs/scratch1/nagarwal/CS696_Stock_fundamental_prediction/sentimentscore/"
#args = parser.parse_args()
files = ["yoy1.csv", "yoy2.csv", "yoy3.csv", "yoy4.csv", "yoy5.csv", "yoy6.csv", "yoy7.csv", "yoy8.csv", "yoy9.csv", "yoy10.csv","yoy11.csv"]
def preprocessText(text):
  "Lower case the text"
  text = (text.encode('ascii', 'ignore')).decode("utf-8") 
  "Remove numbers from the text"
  return text

if not os.path.exists(outputpath):
    os.mkdir(outputpath)

model = BertForSequenceClassification.from_pretrained(model_path,num_labels=3,cache_dir=None)
#now = datetime.datetime.now().strftime("predictions_%B-%d-%Y-%I:%M.csv")
sections = ['item1a', 'item7']
for file in files:
  df = pd.read_csv(inputpath+file)
  for i in range(len(df)):
    row = df.iloc[i]
    filename = row['Ticker'] + '_' + str(int(row["Year"]) +2000) + ".json"
    filepath = os.path.join(outputpath, filename)
    if os.path.exists(filepath):
     continue
    out = {}
    for section in sections:
      text = row[section]
      if type(text) == str:
        text = preprocessText(text)
        score = predict(text,model)
        out[section] = score
      else:
        break
    if len(out.keys())==2:
      f = open(filepath, "w+")
      f.write(json.dumps(out))
      f.close()
