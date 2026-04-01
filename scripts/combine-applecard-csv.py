import os
import logging
import datetime
from pathlib import Path
import time
import sys

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
loglevel = "INFO"

# Call main function
if (__name__ == "__main__"):
    main(scriptname, loglevel, localDev)

logging.critical(scriptname)
currenttime = str(datetime.datetime.now(datetime.timezone.utc))
logging.critical('Start: ' + currenttime)

outputfilename = "apple-card-combined.csv"
# inputPath = "../local/input/applecard/"
# inputPath = Path.home() / "Documents" / "Finances" / "Spending Analysis" / "~data" / "Nance"
inputPath = Path.home() / "Documents" / "Finances" / "Spending Analysis" / "~data" / "Apple-Card"

files = []
files.clear()

filesSkipped = []
filesSkipped.clear()

cardDataList = []
cardDataList.clear()

dictExpected = {'Transaction Date':'', 'Clearing Date':'', 'Description':'', 'Merchant':'', 'Category':'', 'Type':'', 'Amount (USD)':'', 'Purchased By':''}

for filename in os.listdir(inputPath):
    files.append(filename)

files.sort()

failurecount = 0

for file in files:
    success = True
    if file == ".DS_Store":
        continue
    if file == "output":
        continue
    logging.critical(file)
    cardData = commoncsv.loadCscvIntoList(str(inputPath) + "/" + file)
    if cardData != "Folder":
        logging.info("Opening: " + file)
        if cardData is None:
            success = False
            failurecount = failurecount + 1
            break
        for row in cardData:
            for key in dictExpected.keys():
                if not key in row:
                    logging.critical("Missing Key: " + key)
                    failurecount = failurecount + 1
                    success = False
                    break
            if success is True:
                try:
                    row['Transaction Date'] = commondatetime.convertDateToIso8601(row['Transaction Date'])
                except Exception as e:
                    success = False
                    failurecount = failurecount + 1
                    logging.critical("Exception Message Transaction Date: " + repr(e))
                    logging.critical(row)
                    continue
                try:
                    row['Clearing Date'] = commondatetime.convertDateToIso8601(row['Clearing Date'])
                except Exception as e:
                    success = False
                    failurecount = failurecount + 1
                    logging.critical("Exception Message Clearing Date: " + repr(e))
                    logging.critical(row)
                    continue
                # add the row to the dictionary
                if success is True:
                    cardDataList.append(row)
                else:
                    logging.critical('Fail: ' + file)
    if failurecount > 0:
        filesSkipped.append(file)

if failurecount > 0:
    logging.critical("Something went wrong and the output may not be valid so check the script log and / or run with loglevel = INFO.")
    logging.critical("Failure Count = " + str(failurecount))

if len(filesSkipped) > 0:
    logging.critical("Files Skipped: " + str(filesSkipped))

if failurecount == 0 and len(filesSkipped) == 0:

    cardDataList.sort(key=sortByTransactionDate)
    logging.critical('Success')
    logging.critical('Entries Processed: ' + str(len(cardDataList)))
    fields = cardDataList[0].keys()
    outputFilePath = str(inputPath) + "/" +  outputfilename
    commoncsv.writeArrayToCsv(fields, cardDataList, outputFilePath)

currenttime = str(datetime.datetime.now(datetime.timezone.utc))
logging.critical('End: ' + currenttime)
logging.shutdown()