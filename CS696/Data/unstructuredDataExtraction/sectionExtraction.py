from bs4 import BeautifulSoup
import re
from sec_edgar_downloader import Downloader
import pandas as pd
import utils
import shutil
import unicodedata
import logging
logger = logging.getLogger('structured')
itemStartEndMapping = {"item1":"item1a","item1a":"item1b","item1b":"item2", "item2":"item3","item3":"item4","item4":"item5",
                      "item5":"item6", "item6":"item7","item7":"item7a","item7a":"item8", "item8":"item9","item9":"item9a",
                       "item9a":"item9b","item9b":"item10","item10":"item11","item11":"item12","item12":"item13",
                       "item13":"item14","item14":"item15","item15":"item16"}

""" Regexes """
''' Regex to find <DOCUMENT> tags '''
doc_start_pattern = re.compile(r'<DOCUMENT>')
doc_end_pattern = re.compile(r'</DOCUMENT>')

''' Regex to find <TYPE> tag prceeding any characters, terminating at new line '''
type_pattern = re.compile(r'<TYPE>[^\n]+')

''' Common regex to get different sections'''
regex = re.compile(r'(>(\s|&#160;|&nbsp;)*item(\s|&#160;|&nbsp;)*(1(\s|&nbsp;|&#160;|&#160;\(|\(|)*a|6|1(\s|&nbsp;|&#160;|&#160;\(|\(|)*b|7(\s|&nbsp;|&#160;|&#160;\(|\(|)*a|7|8|2|4|3)\.{0,1})', re.I)

class FilingsDownloader:
    
    def __init__(self, downloadPath):
        self.downloadPath = downloadPath
        self.downloader = Downloader(self.downloadPath)
    
    # Download 10 latest 10-K filings for the given company ticker
    def downloadFilings(self, ticker, filing_type="10-K", latest=10):
        self.downloader.get(filing_type, ticker, latest)
    
    def removefilings(self, path):
        shutil.rmtree(path, ignore_errors=True)

class SectionExtraction:
    def __init__(self, doc_type):
        ''' set the location where all the downloaded filings will be saved'''
        
        self.pos_dat = None
        self.doc_type = doc_type
        self.document = {}

    def extractHTMLSections(self, raw_10k):
        
        try:
            ''' Create 3 lists with the span idices for each regex '''

            ''' There are many <Document> Tags in this text file, each as specific exhibit like 10-K, EX-10.17 etc
                 First filter will give us document tag start <end> and document tag end's <start> 
                 We will use this to later grab content in between these tags'''
            doc_start_is = [x.end() for x in doc_start_pattern.finditer(raw_10k)]
            doc_end_is = [x.start() for x in doc_end_pattern.finditer(raw_10k)] 

            ''' Type filter is interesting, it looks for <TYPE> with Not flag as new line, ie terminare there, with + sign
                to look for any char afterwards until new line \n. This will give us <TYPE> followed Section Name like '10-K'
                Once we have have this, it returns String Array, below line will with find content after <TYPE> ie, '10-K' 
                as section names '''
            doc_types = [x[len('<TYPE>'):] for x in type_pattern.findall(raw_10k)]

            ''' Create a loop to go through each section type and save only the 10-K section in the dictionary '''
            for doc_type, doc_start, doc_end in zip(doc_types, doc_start_is, doc_end_is):
                if doc_type == self.doc_type:
                    self.document[doc_type] = raw_10k[doc_start:doc_end]
                    break

            ''' Use finditer to math the regex '''
            matches = regex.finditer(self.document[self.doc_type])

            ''' Create the dataframe '''
            test_df = pd.DataFrame([(x.group(), x.start(), x.end()) for x in matches])

            test_df.columns = ['item', 'start', 'end']
            test_df['item'] = test_df.item.str.lower()

            ''' Get rid of unnesesary charcters from the dataframe '''
            test_df.replace('&#160;ris',' ',regex=True,inplace=True)
            test_df.replace('&#160;unresolve',' ',regex=True,inplace=True)
            test_df.replace('&#160;',' ',regex=True,inplace=True)
            test_df.replace('&nbsp;',' ',regex=True,inplace=True)
            test_df.replace(' ','',regex=True,inplace=True)
            test_df.replace('\.','',regex=True,inplace=True)
            test_df.replace('>','',regex=True,inplace=True)
            test_df.replace('\n','',regex=True,inplace=True)
            test_df.replace('\(','',regex=True,inplace=True)

            ''' Aggregate the different parts of the sane section '''
            self.pos_dat = test_df.groupby(['item']).agg({'start': utils.customsort, 'end': 'max'})
            logger.info("Sections Extracted:{}".format(list(self.pos_dat.index)))
        #     print("send any section name as printed")
            return list(self.pos_dat.index)
        except ValueError as e:
            raise ValueError

    def extractTextFromSection(self, key):
        
        if key in list(self.pos_dat.index):
            if self.doc_type not in self.document:
                logger.info("{} not found".format(document_type))
                ''' Get Item 1a '''
            else:
                end = ""
                original = key
                while True:
                    if original not in itemStartEndMapping.keys():
                        break
                    elif itemStartEndMapping[original] not in list(self.pos_dat.index) or self.pos_dat["start"].loc[key]>= self.pos_dat["start"].loc[itemStartEndMapping[original]]:
                        original = itemStartEndMapping[original]
                    else:
                        end = itemStartEndMapping[original]
                        break
                if len(end) == "0":
                    logger.info("Error Cannnot find End tag for {}".format(key))
                    return 
                else:                
                    item_raw = self.document[self.doc_type][self.pos_dat['start'].loc[key]:self.pos_dat['end'].loc[end]]
                    item_raw_content = BeautifulSoup(item_raw, "lxml")
                    content = item_raw_content.get_text()
                    content = unicodedata.normalize("NFKD", content)
                    content = content.replace("\n", " ")
                    content = content.replace("  ", " ")
                    content = content.lower()
                    return content
        else:
            logger.info("{} not found".format(key))
            return ""
    def extractHTMLSectionsFromLinks(self, raw_10k):
        
        try:
            ''' Create 3 lists with the span idices for each regex '''
            self.document[self.doc_type] = raw_10k
            ''' Use finditer to math the regex '''
            matches = regex.finditer(self.document[self.doc_type])

            ''' Create the dataframe '''
            test_df = pd.DataFrame([(x.group(), x.start(), x.end()) for x in matches])

            test_df.columns = ['item', 'start', 'end']
            test_df['item'] = test_df.item.str.lower()

            ''' Get rid of unnesesary charcters from the dataframe '''
            test_df.replace('&#160;ris',' ',regex=True,inplace=True)
            test_df.replace('&#160;unresolve',' ',regex=True,inplace=True)
            test_df.replace('&#160;',' ',regex=True,inplace=True)
            test_df.replace('&nbsp;',' ',regex=True,inplace=True)
            test_df.replace(' ','',regex=True,inplace=True)
            test_df.replace('\.','',regex=True,inplace=True)
            test_df.replace('>','',regex=True,inplace=True)
            test_df.replace('\n','',regex=True,inplace=True)
            test_df.replace('\(','',regex=True,inplace=True)

            ''' Aggregate the different parts of the sane section '''
            self.pos_dat = test_df.groupby(['item']).agg({'start': utils.customsort, 'end': 'max'})
            logger.info("Sections Extracted:{}".format(list(self.pos_dat.index)))
        #     print("send any section name as printed")
            return list(self.pos_dat.index)
        except ValueError as e:
            raise ValueError
