from os import listdir
from os.path import isfile, join, isdir
import csv
import utils
from sectionExtraction import SectionExtraction, FilingsDownloader
import pandas as pd

exceptions = {'Brookfield Property REIT Inc Class A':1496048, 'Liberty Media Corporation Series A Liberty Formula One':1560385, 'Vistra Energy Corp.':1692819 , 'IAA, Inc.':1745041, 'Gardner Denver Holdings, Inc.':1699150}



def startWriting(downloadPath, tickerList, fieldnames,index=0, latest=10, sections=["item1a", "item7"]):
    ''' Get List of all the folders concatenated with its relative path '''
    companyLessthan10 = []
    companyWithNoData = []
    erroneousCompanies = []
    fieldnames.extend(sections)
#     df = pd.read_csv('../../tickerList.csv')
    df = pd.read_csv(tickerList)
    ''' SEC-Edgar module creates a folder 'sec_edgar_filings' in which it downloades the filings '''
    newPath = join(downloadPath, "sec_edgar_filings")
    companyFilingsPath = ""

    ''' loop through all folders i.e. companies '''

#     with open('../../' + filename, mode='w+', encoding="utf-8", newline='') as file:
#         fieldnames = ['Ticker', "Company Name", "Industry","Top 100","Year","Risk Factors"]
#         writer = csv.DictWriter(file, fieldnames=fieldnames)
#         writer.writeheader()
    writers = utils.createCSVWriters("../../", fieldnames, num=11)
    downloader = FilingsDownloader(downloadPath)
    for i in range(index, len(df)):
        row = df.iloc[i]

#         try:

        ''' Download latest 10 filings for the Company '''
        print("Downloading {} latest Filings for {}".format(latest, row["Company Name"]))
        downloader.downloadFilings(ticker=row['Ticker'], latest = latest)


        ''' SEC-Edgar module creates a subfolder named by the company ticker inside 'sec_edgar_filings'
            Therfore join the path  '''
        companyFilingsPath = join(newPath, row['Ticker'], "10-K")
        print("companyfilingsPath {}".format(companyFilingsPath))


        ''' Sanity Check: if the files are downloaded '''
        if not isdir(companyFilingsPath):
            print("No filings Downloaded for {}".format(row["Company Name"]))
            companyWithNoData.append(row["Company Name"])
            continue


        ''' List downloded filing path and file names '''
        companyFilings = [(join(companyFilingsPath, f), f) for f in listdir(companyFilingsPath)]



        ''' Log the companies having less than 10 recent filings '''
        if len(companyFilings) <10:
            companyLessthan10.append(row["Company Name"])



        ''' Extract Section from each filings '''
        for filing in companyFilings:

            extractor = SectionExtraction()

            line = utils.formLine(fieldnames)
            line["Company Name"] = row["Company Name"]
            line["Industry"] = row["Industry"]
            line["Top 100"] = row["Top 100"]
            line["Ticker"] = row['Ticker']

            ''' Get filing path and filing path '''
            filingPath, filingName = filing

            f = open(filingPath,'r')
            textdata = f.read()
            f.close()
            sectionList = extractor.extractHTMLSections(textdata)

            ''' Get year of the filling from the filing name '''
            ''' file name ex "0001283630-16-000038.txt", 2016 represents year in which 10k was filed and it was for year 2015 '''
            filingName = filingName.split("-")
            line["Year"] = int(filingName[1])-1
            ''' Extracting Sections  '''
            for item in sections:
                if item in sectionList:
                    line[item] = extractor.extractTextFromSection(key =item)
                else:
                    print(" {} not in section list for Company Name: {}, path: {}".format(item, row["Company Name"], filing))
                    #utils.closeWriters(writers)
                    #return i

                if len(line[item]) <100:
                    print("empty text", row["Company Name"], filing)
                    #utils.closeWriters(writers)
                    #return i
                    continue

                print("Extracted Text Length:{}".format(len(line[item])))


            ''' write to csv file '''
            writer_index = int(filingName[1])-10
            if writer_index <0:
                print("Problem with the writer Index",writer_index, filingName, "exiting")
                continue

            writers[writer_index][0].writerow(line)
        downloader.removefilings(join(newPath, row['Ticker']))
#         except Exception as e:
#             erroneousCompanies.append((e, row["Company Name"]))
#             print("Exception {} Occured for {}, skipping".format(e,row["Company Name"]))
    utils.closeWriters(writers)
    return companyLessthan10, companyWithNoData, erroneousCompanies
