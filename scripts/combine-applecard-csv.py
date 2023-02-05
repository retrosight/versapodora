import os
import logging
import datetime
import time

import commoncsv
import commonlogging
from commonlogging import main
import commondatetime


def sortByTransactionDate(e):
    return e['Transaction Date']


localDev = True

# Clear the screen
os.system('cls' if os.name == 'nt' else 'clear')

# Setup logging
scriptname = "combine-applecard-csv"
loglevel = "CRITICAL"

# Call main function
if (__name__ == "__main__"):
    main(scriptname, loglevel, localDev)

logging.critical(scriptname)
currenttime = datetime.datetime.utcnow().isoformat()
logging.critical('Start: ' + currenttime)

localPath = "../local/"
inputath = localPath + "input/"
outputPath = localPath + "output/"

files = []
files.clear()

cardDataDict = []
cardDataDict.clear()

for filename in os.listdir(inputath):
    files.append(filename)

for file in files:
    logging.critical(file)
    cardData = commoncsv.loadCscvIntoArray(inputath + file)
    for row in cardData:
        cardDataDict.append(row)

cardDataDict.sort(key=sortByTransactionDate)

fields = ['Transaction Date', 'Clearing Date', 'Description', 'Merchant', 'Category', 'Type', 'Amount (USD)', 'Purchased By']
commoncsv.writeArrayToCsv(fields, cardDataDict, "apple-card-combined.csv")

currenttime = datetime.datetime.utcnow().isoformat()
logging.critical('End: ' + currenttime)
logging.shutdown()