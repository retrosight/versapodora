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


def sortByClearingDate(e):
    return e['Clearing Date']

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
outputfoldername = "applesavings/"
outputfilename = "apple-savings-combined.csv"
inputPath = localPath + "input/" + outputfoldername
outputPath = localPath + "output/" + outputfoldername

files = []
files.clear()

filesSkipped = []
filesSkipped.clear()

cardDataList = []
cardDataList.clear()

dictExpected = {'Transaction Date':'', 'Posted Date':'', 'Activity Type':'', 'Transaction Type':'', 'Description':'', 'Currency Code':'', 'Amount':''}
# dictExpected = {'Transaction Date':'', 'Clearing Date':'', 'Description':'', 'Merchant':'', 'Category':'', 'Type':'', 'Amount (USD)':''}

for filename in os.listdir(inputPath):
    files.append(filename)

files.sort()

failurecount = 0

# for file in files:
#     logging.critical(file)

for file in files:
    success = True
    if file == ".DS_Store":
        filesSkipped.append(file)
        success = False
        continue
    cardData = commoncsv.loadCscvIntoList(inputPath + file)
    if cardData != "Folder":
        logging.info("Opening: " + file)
        if cardData is None:
            success = False
            failurecount = failurecount + 1
            filesSkipped.append(file)
            break
        for row in cardData:
            # Check to see if all keys are present.
            for key in dictExpected.keys():
                if not key in row:
                    logging.info("Missing Key: " + key)
                    failurecount = failurecount + 1
                    filesSkipped.append(file)
                    success = False
                    break
            if success is True:
                try:
                    transactionDate = commondatetime.convertDateToIso8601(row['Transaction Date'])
                    row['Transaction Date'] = transactionDate
                    postedDate = commondatetime.convertDateToIso8601(row['Posted Date'])
                    # clearingDate = commondatetime.convertDateToIso8601(row['Clearing Date'])
                    row['Posted Date'] = postedDate
                    # row['Clearing Date'] = clearingDate
                except Exception as e:
                    success = False
                    failurecount = failurecount + 1
                    logging.critical("Exception Message: " + repr(e))
                    continue
                # add the row to the dictionary
                if success is True:
                    cardDataList.append(row)
                else:
                    logging.critical('Fail: ' + file)
        logging.critical("Success = " + str(success) + ":  " + file)

cardDataList.sort(key=sortByTransactionDate)

fields = ['Transaction Date', 'Posted Date', 'Activity Type', 'Transaction Type', 'Description', 'Currency Code', 'Amount']
# fields = ['Transaction Date', 'Clearing Date', 'Description', 'Merchant', 'Category', 'Type', 'Amount (USD)', 'Purchased By']
commoncsv.writeArrayToCsv(fields, cardDataList, outputfoldername + outputfilename)

if failurecount > 0:
    logging.critical("Something went wrong and the output may not be valid so check the script log and / or run with loglevel = INFO.")
    logging.critical("Failure Count = " + str(failurecount))

logging.critical("Files Skipped: " + str(filesSkipped))

currenttime = datetime.datetime.utcnow().isoformat()
logging.critical('End: ' + currenttime)
logging.shutdown()