import difflib
import csv
import pandas as pd
from os import listdir
from os.path import isfile, join
import re
folderPath = "./data_10K_3K"
outputFilePath = "./"
outputFileName = "diff.csv"

diffObj = difflib.Differ()
fieldnames = ["Year", "Ticker", "item1a", "item7"]
f_out = open(join(outputFilePath,outputFileName), mode='w+', encoding="utf-8", newline='')
writer = csv.DictWriter(f_out, fieldnames=fieldnames)
writer.writeheader()

files = ["yoy1.csv", "yoy2.csv", "yoy3.csv", "yoy4.csv", "yoy5.csv", "yoy6.csv", "yoy7.csv", "yoy8.csv", "yoy9.csv", "yoy10.csv", "yoy11.csv"]
present = files.pop()
df_present = pd.read_csv(join(folderPath,present))

while len(files)>0:
    previous = files.pop()

    df_previous = pd.read_csv(join(folderPath, previous))
    for i in range(len(df_present)):
        row = df_present.iloc[i]
        current_item1a = row["item1a"]
        current_item7 = row["item7"]
        try:
           if type(current_item1a)== str and type(current_item7)== str and len(current_item1a)>100 and len(current_item7)>100:
                search = df_previous.query('Year=='+ str(int(row["Year"])-1) +' and '+'Ticker=="'+row["Ticker"]+'"')
                if len(search)==0:
                   continue
                previous_item1a = search.iloc[0]["item1a"]
                previous_item7 = search.iloc[0]["item7"]
                if len(previous_item1a)>100 and len(previous_item7)>100:
                   previous_item1a = re.split('\\s+',previous_item1a)
                   #print(previous_item1a)
                   previous_item7 = re.split('\\s+',previous_item7)
                   current_item1a = re.split('\\s+',row["item1a"])
                   current_item7 = re.split('\\s+', row["item7"])
                   diff_item1a = list(diffObj.compare(previous_item1a, current_item1a))
                   #print("------Diff Item1a-----")
                   #print(diff_item1a)
                   added_item1a = []
                   for i in range(len(diff_item1a)):
                       if diff_item1a[i][0] == "+":
                           added_item1a.append(diff_item1a[i][1:])
                   #print("---Added Item 1a----")
                   #print(added_item1a)
                   diff_item7 = list(diffObj.compare(previous_item7, current_item7))
                   added_item7 = []
                   for i in range(len(diff_item7)):
                       if diff_item7[i][0] == "+":
                           added_item7.append(diff_item7[i][1:])
                   writer.writerow({"Ticker": row["Ticker"],"Year":int(row["Year"]) + 2000,"item1a":" ".join(added_item1a), "item7":" ".join(added_item7)})
        except Exception as e:
           print(e)
           print(row)
           continue
           #import sys
           #sys.exit()
       
    df_present = df_previous

f_out.close()
                
                
                
