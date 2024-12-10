import os
import logging
import datetime
import time
import sys
from pathlib import Path
import re

import commoncsv
import commonlogging
from commonlogging import main
import commondatetime


def sortByTransactionDate(e):
    return e['Transaction Date']


def sortByTransactionId(e):
    return e['Transaction ID']


localDev = True

# Clear the screen
os.system('cls' if os.name == 'nt' else 'clear')

# Setup logging
scriptname = "map-data"
loglevel = "CRITICAL"

# Call main function
if (__name__ == "__main__"):
    main(scriptname, loglevel, localDev)

logging.critical(scriptname)
currenttime = str(datetime.datetime.now(datetime.timezone.utc))
logging.critical('Start: ' + currenttime)

inputPath = Path.home() / "Documents" / "Finances" / "fierce-waterfall-data"

bankDataInputFiles = ['ExportedTransactions-9635.csv', 'ExportedTransactions-9494.csv', 'ExportedTransactions-5202.csv', 'ExportedTransactions-4341.csv']
creditDataInputFiles = ['Chase8814_Activity20240101_20241209_20241209.CSV']
dataStripeFilename = "Card_Transactions_Report_For_Fierce_Waterfall_PLLC_2024-12-09_103657.csv"

outputLedger = []
outputLedger.clear()

transactionIds = []

for checkingDataFile in bankDataInputFiles:
    bankDataFilePath = str(inputPath) + "/" + checkingDataFile
    logging.critical(bankDataFilePath)
    checkingdatainput = []
    checkingdatainput.clear()
    checkingdatainput = commoncsv.loadCscvIntoList(bankDataFilePath)
    for transaction in checkingdatainput:
        transaction['Posting Date'] = commondatetime.convertDateToIso8601(transaction['Posting Date'])
        transaction['Effective Date'] = commondatetime.convertDateToIso8601(transaction['Effective Date'])
        quarter = transaction['Posting Date']
        quarter = quarter[5:7]
        transaction['Quarter'] = commondatetime.getCalendarQuarter(quarter)
        transaction['Year'] = transaction['Posting Date'][0:4]
        transaction['Amount'] = "{:.2f}".format(round(float(transaction['Amount']), 2))
        transaction['Balance'] = "{:.2f}".format(round(float(transaction['Balance']), 2))
        transaction['Category Type'] = ""
        transaction['Category'] = ""
        transaction['Account'] = checkingDataFile
        if transaction['Transaction ID'] not in transactionIds:
            transactionIds.append(transaction['Transaction ID'])
        else:
            logging.critical('Checking - Created reference for Transaction ID is a duplicate: ' + checkingDataFile + ' | ' + transaction['Transaction ID'])
        outputLedger.append(transaction)

creditdatainput = []
creditdatainput.clear()
creditdatainput = commoncsv.loadCscvIntoList(str(inputPath) + "/" + creditDataInputFiles[0])

for transactionCredit in creditdatainput:
    success = False

    transactionCredit['Posting Date'] = commondatetime.convertDateToIso8601(transactionCredit['Post Date'])
    
    transactionCredit['Effective Date'] = commondatetime.convertDateToIso8601(transactionCredit['Transaction Date'])
    
    reference = transactionCredit['Card'] + transactionCredit['Transaction Date'] + transactionCredit['Post Date'] + transactionCredit['Description'] + transactionCredit['Category'] + transactionCredit['Type'] + transactionCredit['Amount']
    reference = reference.replace('/', '')
    reference = reference.replace('*', '')
    reference = reference.replace(' ', '')
    reference = reference.replace('-', '')
    reference = reference.replace('.', '')
    reference = transactionCredit['Posting Date'].replace('-', '') + ' ' + reference
    # logging.critical(reference)
    
    if reference not in transactionIds:
        transactionIds.append(reference)
    else:
        logging.critical('Created reference for Transaction ID is a duplicate. Exiting.')
        sys.exit()
    transactionCredit['Transaction ID'] = reference

    del transactionCredit['Post Date']
    del transactionCredit['Transaction Date']
    transactionCredit['Transaction Type'] = ''

    transactionCredit['Amount'] = "{:.2f}".format(round(float(transactionCredit['Amount']), 2))

    transactionCredit['Check Number'] = ''

    transactionCredit['Reference Number'] = ''

    # Description already a part of the data set.

    transactionCredit['Transaction Category'] = transactionCredit['Category']
    del transactionCredit['Category']

    # Type is already a part of the data set.

    transactionCredit['Balance'] = ''
    
    # Memo is already a part of the data set.
    
    transactionCredit['Extended Description'] = ''

    transactionCredit['Category Type'] = ""
    
    transactionCredit['Category'] = ""

    transactionCredit['Year'] = transactionCredit['Posting Date'][0:4]

    quarter = transactionCredit['Posting Date']
    quarter = quarter[5:7]
    transactionCredit['Quarter'] = commondatetime.getCalendarQuarter(quarter)

    transactionCredit['Account'] = 'ExportedTransactions-Chase-8814.csv'
    del transactionCredit['Card']
    outputLedger.append(transactionCredit)

outputLedger.sort(key=sortByTransactionId)

logging.critical(len(outputLedger))

regexMaps = []
regexMaps.clear()
regexMaps = commoncsv.loadCscvIntoList(str(inputPath) + "/" + 'regex-map.csv')

venmoAndCheckTransactions = []
venmoAndCheckTransactions.clear()
venmoAndCheckTransactions = commoncsv.loadCscvIntoList(str(inputPath) + "/" + 'venmo-and-check-map.csv')

descriptionList = []
descriptionList.clear()

allDescriptions = []
allDescriptions.clear()

for transactionLedger in outputLedger:
    foundRegexMatch = False
    matchCategoryTypeResult = ''
    matchCategoryResult = ''
    for regexMap in regexMaps:
        currentPattern = rf"{regexMap['pattern']}"
        if regexMap['group'] != '':
            currentGroup = int(regexMap['group'])
        else:
            currentGroup = 0
        currentGroupResult = regexMap['groupresult']
        currentUuid = regexMap['uuid']
        matchPattern = re.match(currentPattern, transactionLedger['Description'])
        if matchPattern:
            # logging.critical(currentGroup)
            # logging.critical(currentUuid)
            if currentGroup != 0:
                matchGroup = matchPattern.group(currentGroup)
                if matchGroup == currentGroupResult:
                    matchCategoryTypeResult = regexMap['categorytype']
                    matchCategoryResult = regexMap['category']
                    foundRegexMatch = True
            else:
                # logging.critical(regexMap['categorytype'])
                matchCategoryTypeResult = regexMap['categorytype']
                matchCategoryResult = regexMap['category']
                foundRegexMatch = True
    transactionLedger['Category Type'] = matchCategoryTypeResult
    transactionLedger['Category'] = matchCategoryResult

    if transactionLedger['Category'] == '' and transactionLedger['Category Type'] == '':
        for venmoAndCheckTransaction in venmoAndCheckTransactions:
            if venmoAndCheckTransaction['Transaction ID'] == transactionLedger['Transaction ID']:
                transactionLedger['Category'] = venmoAndCheckTransaction['category']
                transactionLedger['Category Type'] = venmoAndCheckTransaction['categorytype']
                break

    # logging.critical(transactionLedger)
    if transactionLedger['Description'] not in allDescriptions and foundRegexMatch is False:
        currentDescription = {}
        currentDescription.clear()
        currentDescription['Description'] = transactionLedger['Description']
        descriptionList.append(currentDescription)
        allDescriptions.append(transactionLedger['Description'])

fields = outputLedger[0].keys()
commoncsv.writeArrayToCsv(fields, outputLedger, str(inputPath) + "/outputLedger.csv")

if len(descriptionList) > 0:
    descriptionFields = descriptionList[0].keys()
    commoncsv.writeArrayToCsv(descriptionFields, descriptionList, str(inputPath) + "/descriptionList.csv")

categories = []
categories.clear()

blankCategories = False
for transactionLedger in outputLedger:
    if transactionLedger['Category'] == '':
        blankCategories = True
    if transactionLedger['Category'] not in categories:
        categories.append(transactionLedger['Category'])

categories.sort()

years = ['2023','2024','2025']
quarters = ['Q1', 'Q2', 'Q3', 'Q4']

bankingCategoryTotals = []
bankingCategoryTotals.clear()

if blankCategories is False:
    for year in years:
        for quarter in quarters:
            for category in categories:
                totalForCategory = 0
                for ledgertransaction in outputLedger:
                    if ledgertransaction['Category'] == category and ledgertransaction['Year'] == year and ledgertransaction['Quarter'] == quarter:
                        currentvalue = 0
                        currentvalue = ledgertransaction['Amount']
                        totalForCategory += float(currentvalue)
                currentCategoryTotal ={}
                currentCategoryTotal.clear()
                currentCategoryTotal['category'] = category
                currentCategoryTotal['total'] = "{:.2f}".format(round(totalForCategory,2))
                currentCategoryTotal['year'] = year
                currentCategoryTotal['quarter'] = quarter
                bankingCategoryTotals.append(currentCategoryTotal)

    outputTotalFields = ['category', 'total', 'year', 'quarter']
    commoncsv.writeArrayToCsv(outputTotalFields, bankingCategoryTotals, str(inputPath) + "/ledgerChecking-category-totals.csv")
else:
    logging.critical("**** WARNING! Blank categories -- update data to update the totals. ****")

# Stripe Transactions

dataStripe = commoncsv.loadCscvIntoList(str(inputPath) + "/" +  dataStripeFilename)

stripeList = []
stripeList.clear()

for rowStripe in dataStripe:
    rowStripe.pop('Client name')
    rowStripe['Created (UTC)'] = commondatetime.convertAnotherDateToIso8601(rowStripe['Created (UTC)'])
    rowStripe['Available On (UTC)'] = commondatetime.convertAnotherDateToIso8601(rowStripe['Available On (UTC)'])
    quarter = rowStripe['Created (UTC)']
    quarter = quarter[5:7]
    rowStripe['Quarter'] = commondatetime.getCalendarQuarter(quarter)
    rowStripe['Year'] = rowStripe['Created (UTC)'][0:4]
    stripeSsuccess = True
    stripeList.append(rowStripe)

stripeList.sort(key=sortByTransactionId)
fieldsStripe = stripeList[0].keys()
commoncsv.writeArrayToCsv(fieldsStripe, stripeList, str(inputPath) + "/" +  "output-" + dataStripeFilename)

outputStripeTotals = []
outputStripeTotals.clear()

for year in years:
    for quarter in quarters:
        totalForStripeAmount = 0
        totalForStripeFee = 0
        for stripeDataRow in stripeList:
            if stripeDataRow['Transaction Type'] == "charge" and stripeDataRow['Year'] == year and stripeDataRow['Quarter'] == quarter:
                totalForStripeAmount += float(stripeDataRow['Amount'])
                totalForStripeFee += float(stripeDataRow['Fee'])
        currentStripeTotal ={}
        currentStripeTotal.clear()
        currentStripeTotal['totalamount'] = "{:.2f}".format(round(totalForStripeAmount,2))
        currentStripeTotal['totalfee'] = "{:.2f}".format(round(totalForStripeFee,2))
        currentStripeTotal['year'] = year
        currentStripeTotal['quarter'] = quarter
        outputStripeTotals.append(currentStripeTotal)

outputStripeTotalFields = ['totalamount', 'totalfee', 'year', 'quarter']
commoncsv.writeArrayToCsv(outputStripeTotalFields, outputStripeTotals, str(inputPath) + "/" + "output-Card_Transactions-totals.csv")

currenttime = str(datetime.datetime.now(datetime.timezone.utc))
logging.critical('End: ' + currenttime)
logging.shutdown()