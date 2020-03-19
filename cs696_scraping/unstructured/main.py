import writer

if __name__== "__main__":
    downloadPath = "../../"
    fieldnames = ['Ticker', "Company Name", "Industry","Top 100","Year"]
    tickerList = "../../tickerList.csv"
    writer.startWriting(downloadPath, tickerList, fieldnames)