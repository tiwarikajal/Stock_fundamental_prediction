import writer
import json
import logging
from datetime import datetime

if __name__== "__main__":
    dateTimeObj = datetime.now()
    logger = logging.getLogger('structured')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('structured.log')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    downloadPath = "../../"
#     fieldnames = ["Year","Company", "Industry","Top 100"]
    fieldnames = ["CIK","DocIndex", "IndexLink", "Description","Form10KName","Year"]
#     tickerList = "../../tickerList3K.csv"
    tickerList = "../../10kList.csv"
    logger.info("Start Time: "+str(dateTimeObj))
    writer.startWriting(downloadPath, tickerList, fieldnames,links=True,latest=10, index=0,  sections=["item1a", "item7"], doc_type = "10-K")
#     downloadPath, tickerList, fieldnames,index=0, latest=10, sections=["item1a", "item7"], doc_type = "10-K"
#     companyLessthan10, companyWithNoData, erroneousCompanies,dataStats = writer.startWriting(downloadPath, tickerList, fieldnames,links=True,latest=10, index=0,  sections=["item1a", "item7"], doc_type = "10-K")
#     f = open("dataStats.txt","w+")
#     f.write(json.dumps(dataStats))
#     f.close()
#     f = open("companyLessthan10.txt","w+")
#     f.write(str(companyLessthan10))
#     f.close()
#     f = open("companyWithNoData.txt","w+")
#     f.write(str(companyWithNoData))
#     f.close()
#     f = open("erroneousCompanies.txt","w+")
#     f.write(str(erroneousCompanies))
#     f.close()
    
       
    dateTimeObj = datetime.now()
    logger.info("End Time: "+str(dateTimeObj))


    