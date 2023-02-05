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
inputPath = localPath + "input/"
outputPath = localPath + "output/"

files = []
files.clear()

cardDataList = []
cardDataList.clear()

dictExpected = {'Transaction Date':'', 'Clearing Date':'', 'Description':'', 'Merchant':'', 'Category':'', 'Type':'', 'Amount (USD)':'', 'Purchased By':''}

for filename in os.listdir(inputPath):
    files.append(filename)

files.sort()

failurecount = 0

for file in files:
    success = True
    cardData = commoncsv.loadCscvIntoList(inputPath + file)
    if cardData is None:
        success = False
        failurecount = failurecount + 1
    try:
        for row in cardData:
            # Check to see if all keys are present.
            for key in dictExpected.keys():
                if not key in row:
                    logging.info("Missing Key: " + key)
            try:
                # Convert the mm/dd/yyyy in the original CSV to YYYY-MM-DD
                # according to the ISO 8601 standard
                # https://en.wikipedia.org/wiki/ISO_8601 Calendar dates
                transactionDate = row['Transaction Date']
                transactionDate = datetime.datetime.strptime(transactionDate, "%m/%d/%Y")
                row['Transaction Date'] = str(transactionDate)[0:10]
                clearingDate = row['Clearing Date']
                clearingDate = datetime.datetime.strptime(clearingDate, "%m/%d/%Y")
                row['Clearing Date'] = str(clearingDate)[0:10]
            except Exception as e:
                success = False
                failurecount = failurecount + 1
                logging.critical("Exception Message: " + repr(e))
                continue
            # add the row to the dictionary
            if success is True:
                cardDataList.append(row)
    except Exception as e:
        success = False
        failurecount = failurecount + 1
        logging.critical("Exception Message: " + repr(e))
        continue
    if success is True:
        logging.critical('Success: ' + file)
    else:
        logging.critical('Fail: ' + file)

cardDataList.sort(key=sortByTransactionDate)

fields = ['Transaction Date', 'Clearing Date', 'Description', 'Merchant', 'Category', 'Type', 'Amount (USD)', 'Purchased By']
commoncsv.writeArrayToCsv(fields, cardDataList, "apple-card-combined.csv")

if failurecount > 0:
    logging.critical("Something went wrong and the output may not be valid so check the script log and / or run with loglevel = INFO.")
    logging.critical("Failure Count = " + str(failurecount))

currenttime = datetime.datetime.utcnow().isoformat()
logging.critical('End: ' + currenttime)
logging.shutdown()