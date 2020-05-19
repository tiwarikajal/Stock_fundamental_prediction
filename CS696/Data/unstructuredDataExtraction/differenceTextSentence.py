import difflib
import csv
import pandas as pd
from os import listdir
from os.path import isfile, join
import re
from nltk.tokenize import sent_tokenize, word_tokenize
import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stopwords = stopwords.words('english')

def clean_string(text):
    text = word_tokenize(text)
    text = [word for word in text if word not in string.punctuation]
    text = ' '.join([word for word in text if word not in stopwords])
    return text


def cosine_sim_vectors(vec1, vec2):
 vec1 = vec1.reshape(1,-1)
 vec2 = vec2.reshape(1, -1)
 return cosine_similarity(vec1, vec2)[0][0]

folderPath = "./data_10K_3K"
outputFilePath = "./"
outputFileName = "diffSentence.csv"

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
            if type(current_item1a) == str and type(current_item7) == str and len(current_item1a)>100 and len(current_item7)>100:
                search = df_previous.query('Year=='+ str(int(row["Year"])-1) +' and '+'Ticker=="'+row["Ticker"]+'"')
                previous_item1a = search.iloc[0]["item1a"]
                previous_item7 = search.iloc[0]["item7"]
                if len(previous_item1a)>100 and len(previous_item7)>100:
                    previous_item1a = sent_tokenize(previous_item1a)
                    #print(previous_item1a)
                    previous_item7 = sent_tokenize(previous_item7)
                    current_item1a = sent_tokenize(current_item1a)
                    current_item7 = sent_tokenize(current_item7)
                    diff_item1a = list(diffObj.compare(previous_item1a, current_item1a))
                    added_item1a = []
                    for i in range(len(diff_item1a)):
                        if diff_item1a[i][0] == "+" or diff_item1a[i][0] == "-":
                            added_item1a.append(diff_item1a[i][1:])
                    final_item1a = []
                    for i in range(len(added_item1a)):
                        new_added_item1a = added_item1a[:i] + added_item1a[i+1:]
                        line = added_item1a[i]
                        line1 = clean_string(line)
                        overallsimilarityScore = 0
                        for compline in new_added_item1a:
                            line2 = clean_string(compline)
                            vectorizer = CountVectorizer().fit_transform([line1, line2])
                            vectors = vectorizer.toarray()
                            similarityScore = cosine_sim_vectors(vectors[0], vectors[1])
                            print("Similarity Score:{}".format(similarityScore))
                            if similarityScore>overallsimilarityScore:
                                overallsimilarityScore = similarityScore
                        print("Overall Similarity Score:{}".format(overallsimilarityScore))
                        if overallsimilarityScore<=0.40:
                            final_item1a.append(line)
                    print("Final Item 1A: {}".format(" ".join(final_item1a)))
                    print("Diff Item 1a: {}".format(" ".join(added_item1a)))
                    diff_item7 = list(diffObj.compare(previous_item7, current_item7))
                    added_item7 = []
                    for i in range(len(diff_item7)):
                        if diff_item7[i][0] == "+" or diff_item7[i][0] == "-":
                            added_item7.append(diff_item7[i][1:])
                    final_item7 = []
                    for i in range(len(added_item7)):
                        new_added_item7 = added_item7[:i] + added_item7[i+1:]
                        line = added_item7[i]
                        line1 = clean_string(line)
                        overallsimilarityScore = 0
                        for compline in new_added_item7:
                            line2 = clean_string(compline)
                            vectorizer = CountVectorizer().fit_transform([line1, line2])
                            vectors = vectorizer.toarray()
                            similarityScore = cosine_sim_vectors(vectors[0], vectors[1])
                            if similarityScore>overallsimilarityScore:
                                overallsimilarityScore = similarityScore
                        if overallsimilarityScore<=0.40:
                            final_item7.append(line)
                    writer.writerow({"Ticker": row["Ticker"],"Year":int(row["Year"]) + 2000,"item1a":" ".join(final_item1a), "item7":" ".join(final_item7)})
        except Exception as e:
           print(e)
           print(row)
           #break
           continue
    df_present = df_previous
f_out.close()
                
                
                
