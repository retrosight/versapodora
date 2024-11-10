import os
import logging
import datetime
import time
import sys

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
currenttime = str(datetime.datetime.now(datetime.UTC))
logging.critical('Start: ' + currenttime)

localPath = "../local/"
inputPath = localPath + "input/fierce/"
outputPath = localPath + "output/fierce/"

# Data inputs
# checkingdatainput = commoncsv.loadCscvIntoList(inputPath + "ExportedTransactions-9635.csv")
# checkingForRentInput = commoncsv.loadCscvIntoList(inputPath + 'ExportedTransactions-4341.csv')

checkingDataInputFiles = ['ExportedTransactions-9635.csv', 'ExportedTransactions-4341.csv']

# Mapping inputs
categorymapping = commoncsv.loadCscvIntoList(inputPath + "categorymapping.csv")
categorymappingstartswith = commoncsv.loadCscvIntoList(inputPath + "categorymapping-startswith.csv")

# Outputs
outputledger = commoncsv.loadCscvIntoList(outputPath + "output-ledgerChecking.csv")

transactionIds = []

for checkingDataFile in checkingDataInputFiles:
    checkingdatainput = []
    checkingdatainput.clear()
    checkingdatainput = commoncsv.loadCscvIntoList(inputPath + checkingDataFile)
    for transaction in checkingdatainput:
        success = False
        try:
            transaction['Posting Date'] = commondatetime.convertDateToIso8601(transaction['Posting Date'])
            transaction['Effective Date'] = commondatetime.convertDateToIso8601(transaction['Effective Date'])
            quarter = transaction['Posting Date']
            quarter = quarter[5:7]
            transaction['Quarter'] = commondatetime.getCalendarQuarter(quarter)
            transaction['Year'] = transaction['Posting Date'][0:4]
            transaction['Amount'] = "{:.2f}".format(round(float(transaction['Amount']), 2))
            transaction['Balance'] = "{:.2f}".format(round(float(transaction['Balance']), 2))
            transaction['Category'] = ""
            transaction['Category Type'] = ""
            transaction['Account'] = checkingDataFile
            if transaction['Transaction ID'] not in transactionIds:
                transactionIds.append(transaction['Transaction ID'])
            else:
                logging.critical('Checking - Created reference for Transaction ID is a duplicate: ' + checkingDataFile + ' | ' + transaction['Transaction ID'])
            success = True
        except Exception as e:
            success = False
            logging.critical("Exception Message: " + repr(e))
            continue
        if success is True:
            inLedger = False
            for ledgertransaction in outputledger:
                if ledgertransaction['Reference Number'] == transaction['Reference Number']:
                    inLedger = True
                    break
            if inLedger == False:
                outputledger.append(transaction)

creditdatainput = []
creditdatainput.clear()
creditdatainput = commoncsv.loadCscvIntoList(inputPath + 'ExportedTransactions-Chase-8814.csv')

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

    success = True
    # except Exception as e:
    #     success = False
    #     logging.critical("Exception Message: " + repr(e))
    #     continue
    if success is True:
        inLedger = False
        for ledgertransaction in outputledger:
            if ledgertransaction['Transaction ID'] == transactionCredit['Transaction ID']:
                inLedger = True
                break
        if inLedger == False:
            outputledger.append(transactionCredit)
            # logging.info('Do Nothing')

outputledger.sort(key=sortByTransactionId)

checkingCategoryTotals = []
checkingCategoryTotals.clear()

categories = []
categories.clear()

blankCategories = False
for ledgertransaction in outputledger:
    for mapstartswith in categorymappingstartswith:
        descriptionToCategorize = mapstartswith['DescriptionToCategorize']
        if ledgertransaction['Description'].startswith(descriptionToCategorize):
            evalTransactionCategory = mapstartswith['EvalTransactionCategory']
            if ledgertransaction['Category Type'] == '':
                ledgertransaction['Category Type'] = mapstartswith['CategoryType']
            if ledgertransaction['Category'] == '':
                ledgertransaction['Category'] = mapstartswith['Category']
            if evalTransactionCategory == "TRUE":
                if ledgertransaction['Category'] == '':
                    ledgertransaction['Category'] = ledgertransaction['Transaction Category']
            break
    for map in categorymapping:
        descriptionToCategorize = map['DescriptionToCategorize']
        if ledgertransaction['Description'] == descriptionToCategorize:
            evalTransactionCategory = map['EvalTransactionCategory']
            if ledgertransaction['Category Type'] == '':
                ledgertransaction['Category Type'] = map['CategoryType']
            if ledgertransaction['Category'] == '':
                ledgertransaction['Category'] = map['Category']
            if evalTransactionCategory == "TRUE":
                if ledgertransaction['Category'] == '':
                    ledgertransaction['Category'] = ledgertransaction['Transaction Category']
            break
    if ledgertransaction['Category Type'] == "" or ledgertransaction['Category'] == "":
        blankCategories = True
    if ledgertransaction['Category'] not in categories:
        categories.append(ledgertransaction['Category'])

# fields = outputledger[0].keys()
fields = ['Transaction ID', 'Posting Date', 'Effective Date', 'Transaction Type', 'Amount', 'Check Number', 'Reference Number', 'Description', 'Transaction Category', 'Type', 'Balance', 'Memo', 'Extended Description', 'Category Type', 'Category', 'Year', 'Quarter', 'Account']
commoncsv.writeArrayToCsv(fields, outputledger, "fierce/output-ledgerChecking.csv")

categories.sort()

years = ['2023','2024','2025']
quarters = ['Q1', 'Q2', 'Q3', 'Q4']

if blankCategories is False:
    for year in years:
        for quarter in quarters:
            for category in categories:
                totalForCategory = 0
                for ledgertransaction in outputledger:
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
                checkingCategoryTotals.append(currentCategoryTotal)

    outputTotalFields = ['category', 'total', 'year', 'quarter']
    commoncsv.writeArrayToCsv(outputTotalFields, checkingCategoryTotals, "fierce/output-" + "ledgerChecking-category-totals.csv")
else:
    logging.critical("Blank categories -- update data to update the totals.")

# Stripe Transactions

dataStripeFilename = "Card_Transactions_Report_For_Fierce_Waterfall_PLLC_2024-11-02_100157.csv"
dataStripe = commoncsv.loadCscvIntoList(inputPath + dataStripeFilename)

stripeList = []
stripeList.clear()

for rowStripe in dataStripe:
    stripeSsuccess = False
    try:
        rowStripe.pop('Client name')
        rowStripe['Created (UTC)'] = commondatetime.convertAnotherDateToIso8601(rowStripe['Created (UTC)'])
        rowStripe['Available On (UTC)'] = commondatetime.convertAnotherDateToIso8601(rowStripe['Available On (UTC)'])
        quarter = rowStripe['Created (UTC)']
        quarter = quarter[5:7]
        rowStripe['Quarter'] = commondatetime.getCalendarQuarter(quarter)
        rowStripe['Year'] = rowStripe['Created (UTC)'][0:4]
        stripeSsuccess = True
    except Exception as e:
        success = False
        logging.critical("Exception Message: " + repr(e))
        continue
    if success is True:
        stripeList.append(rowStripe)

stripeList.sort(key=sortByTransactionId)

fieldsStripe = ['Transaction ID', 'Transaction Type', 'Source', 'Amount', 'Fee', 'Net', 'Currency', 'Created (UTC)', 'Available On (UTC)', 'Quarter', 'Year']
commoncsv.writeArrayToCsv(fieldsStripe, stripeList, "fierce/output-" + dataStripeFilename)

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
commoncsv.writeArrayToCsv(outputStripeTotalFields, outputStripeTotals, "fierce/output-Card_Transactions-totals.csv")

currenttime = str(datetime.datetime.now(datetime.UTC))
logging.critical('End: ' + currenttime)
logging.shutdown()