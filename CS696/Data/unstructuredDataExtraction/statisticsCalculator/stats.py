from nltk.tokenize import sent_tokenize, word_tokenize
import os
import pandas as pd
import re
import numpy as np
inp_path = "/mnt/nfs/scratch1/nagarwal/CS696_Stock_fundamental_prediction/data_10K_3K/"

files = os.listdir(inp_path)
num_sentences_item1a = []
num_sentences_item7 = []
sentences_per_doc = []
sentence_length = []
sentence_length_item1a = []
sentence_length_item7 = []
unique_words = set()
total_words = 0
def preprocessData(text):
    text = (text.encode('ascii', 'ignore')).decode("utf-8")
    text = re.sub(r'[^\w\s.]','',text)
    return text

def getWords(sentences):
    words = set()
    count = 0
    temp_sentence_length = [] 
    for s in sentences:
        temp_words = word_tokenize(s)
        words.update(temp_words)
        count += len(temp_words)
        temp_sentence_length.append(len(temp_words))
    return list(words), count, temp_sentence_length
    
for file in files:
    filePath = os.path.join(inp_path, file)
    df = pd.read_csv(filePath)
    for i in range(len(df)):
        row = df.iloc[i]
        item1a = row["item1a"]
        item7 = row["item7"]
        word_count = 0
        sentences = None
        sentence_count_item1a = 0
        sentence_count_item7 = 0
        temp_sentence_length = None
        if type(item1a) == str:
            item1a = preprocessData(item1a)
            sentences = sent_tokenize(item1a)
            num_sentences_item1a.append(len(sentences))
            sentence_count_item1a = len(sentences)
            words_item1a, word_count, temp_sentence_length = getWords(sentences)
            total_words += word_count
            unique_words.update(words_item1a)
            sentence_length.extend(temp_sentence_length)
            sentence_length_item1a.extend(temp_sentence_length)
        word_count = 0
        temp_sentence_length = None
        sentences = None
        if type(item7) == str:
            item7 = preprocessData(item7)
            sentences = sent_tokenize(item7)
            num_sentences_item7.append(len(sentences))
            sentence_count_item7 = len(sentences)
            words_item7, word_count, temp_sentence_length = getWords(sentences)
            total_words += word_count
            unique_words.update(words_item7)
            sentence_length.extend(temp_sentence_length)
            sentence_length_item7.extend(temp_sentence_length)
        if sentence_count_item1a>0 or sentence_count_item7>0:
            sentences_per_doc.append(sentence_count_item1a+sentence_count_item7)
        break
#num_sentences_item1a = []
#num_sentences_item7 = []
#sentences_per_doc = []
#sentence_length = []
#unique_words = set()
#total_words = 0
#sentence_length_item1a = []
#sentence_length_item7 = []

num_sentences_item1a = np.array(num_sentences_item1a)
num_sentences_item7 = np.array(num_sentences_item1a)
sentences_per_doc = np.array(sentences_per_doc)
sentence_length = np.array(sentence_length)
sentence_length_item1a = np.array(sentence_length_item1a)
sentence_length_item7 = np.array(sentence_length_item7)

print("Total Words in the Corpus:{}".format(total_words))
print("Total Unique Words in the Corpus:{}".format(len(unique_words)))
print("Average Number of Sentences Per Document:{}".format(np.mean(sentences_per_doc)))
print("Average Number of Sentences in Item1a:{}".format(np.mean(num_sentences_item1a)))
print("Average Number of Sentences in Item7:{}".format(np.mean(num_sentences_item7)))
print("Average Sentence Length in Item1a:{}".format(np.mean(sentence_length_item1a)))
print("Average Sentence Length in Item7:{}".format(np.mean(sentence_length_item7)))
print("Average Sentence Length Combining both the sections:{}".format(np.mean(sentence_length)))





