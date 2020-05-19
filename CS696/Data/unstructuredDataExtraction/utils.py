'''
Some of the code is taken from the finBERT github Repo 
https://github.com/psnonis/FinBERT and modified for the further use
    
'''
import re
from bs4 import BeautifulSoup
import shutil
import os
import csv

def parse_10k(filepath, cik, year):
    """
    Parses the 10-K passed. Returns a 10-K text:
    :param filepath:
    :return: 10-K text without any tables
    """


    with open(filepath) as fp:
        soup = BeautifulSoup(fp, "lxml")

        return __parse_documents(soup)


def __parse_documents(soup):

    documents = soup.find_all('document')

    for doc in documents:

        type_node = doc.find('type')
        if type_node:
            type_text = type_node.contents[0].strip()
            desc_node = type_node.find('description')
        else:
            type_text = 'NA'

        if type_text.startswith("10-K"):
            is_10_k = True
        else:
            continue
        
        if type_text not in ["XML", "GRAPHIC", "EXCEL", "ZIP"]:
            return __extract_document_text(doc)
    return ""

"""
Function to remove tables and give out text
"""
def __extract_document_text(document):

    tables = document.find_all('table')
    for table in tables:
        table.decompose()

    return document.get_text()
"""
Function to sort the seris pandas dataframe and return
the second highest value in the series
param: x: pandas series object

return: the second smallest number 
"""
def customsort(x):
    x = x.values
    if len(x)>1:
        x.sort()
        return x[1]
    else:
        return x[0]

"""
Function to download the filings
param: downloaderObject: sec edgar downloader object
       ticker: string ticker symbol
       filing_type: string, type of filing 10-K/10-Q etc
       latest: int number of latest filings to download
       
return: None
"""
def downloadFilings(downloaderObject, ticker, filing_type="10-K", latest=10):
    downloaderObject.get(filing_type, ticker, latest)

"""
Function to remove downloaded filings
param: path:string path from where the downloaded filings are to be removed
return: None
"""
def removefilings(path):
    shutil.rmtree(path, ignore_errors=True)

"""
Function to create csv writer files
param: path: string , where the csv files will be created
       fieldnames: list, header of all the csv files
       num: int, number of csv files to create, default to 10
       
return: list of tuples, where first element of each tuple is the csv dict writer object and second is the file object
"""
def createCSVWriters(path, fieldnames,num, filename):
    writers = []
    for i in range(num):
        f = open(os.path.join(path,filename + ".csv"), mode='w+', encoding="utf-8", newline='')
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writers.append([writer,f])
    return writers
"""
Function to close all the csv files
param: writer: list of tuples
return: None
"""
def closeWriters(writers):
    for i in range(len(writers)):
        writers[i][1].close()

def formLine(fieldnames):
    line = {}
    for name in fieldnames:
        line[name] = ""
    return line
