import datetime
import time
import logging

commonLocalDev = False

def standardizetime(input):

    currenttimeConverted = str(input)
    currenttimeConverted = currenttimeConverted[0:10]
    currenttimeConverted = datetime.datetime.strptime(currenttimeConverted, "%Y-%m-%d")

    return currenttimeConverted


def roadmapdate(input):

    if input != "None":
        currenttimeConverted = str(input)
        year = currenttimeConverted[0:4]
        month = getmonththreechars(currenttimeConverted[5:7])
        result = month + " " + year

    else:
        result = input

    return result


def roadmapfiscalyearandquarter(input):

    if input != "None":

        fiscalyear = ""
        quarter = ""
        
        inputConvertedToDate = datetime.datetime.strptime(input, '%Y-%m-%d').date()

        inputEpoch = int(inputConvertedToDate.strftime('%s'))

        fiscalyear = ""

        if 1654041600 <= inputEpoch <= 1685577599:
            fiscalyear = "FY23"
            if 1654041600 <= inputEpoch <= 1661990399:
                quarter = "FY23 Q1"
            elif 1661990400 <= inputEpoch <= 1669852799:
                quarter = "FY23 Q2"
            elif 1669852800 <= inputEpoch <= 1677628799:
                quarter = "FY23 Q3"
            elif 1677628800 <= inputEpoch <= 1685577599:
                quarter = "FY23 Q4"
        elif 1685577600 <= inputEpoch <= 1717199999:
            fiscalyear = "FY24"
            if 1685577600 <= inputEpoch <= 1693526399:
                quarter = "FY24 Q1"
            elif 1693526400 <= inputEpoch <= 1701388799:
                quarter = "FY24 Q2"
            elif 1701388800 <= inputEpoch <= 1709164799:
                quarter = "FY24 Q3"
            elif 1709251200 <= inputEpoch <= 1717199999:
                quarter = "FY24 Q4"
        elif 1717200000 <= inputEpoch <= 1748735999:
            fiscalyear = "FY25"
            if 1717200000 <= inputEpoch <= 1725148799:
                quarter = "FY25 Q1"
            elif 1725148800 <= inputEpoch <= 1733011199:
                quarter = "FY25 Q2"
            elif 1733011200 <= inputEpoch <= 1740787199:
                quarter = "FY25 Q3"
            elif 1740787200 <= inputEpoch <= 1748735999:
                quarter = "FY23 Q4"

        resultFiscalYear = fiscalyear
        resultQuarter = quarter

    else:
        resultFiscalYear = "None"
        resultQuarter = "None"

    return resultFiscalYear, resultQuarter


def getmonththreechars(monthvalue):

    result = ""

    if monthvalue == "01":
        result = "Jan"
    if monthvalue == "02":
        result = "Feb"
    if monthvalue == "03":
        result = "Mar"
    if monthvalue == "04":
        result = "Apr"
    if monthvalue == "05":
        result = "May"
    if monthvalue == "06":
        result = "Jun"
    if monthvalue == "07":
        result = "Jul"
    if monthvalue == "08":
        result = "Aug"
    if monthvalue == "09":
        result = "Sep"
    if monthvalue == "10":
        result = "Oct"
    if monthvalue == "11":
        result = "Nov"
    if monthvalue == "12":
        result = "Dec"

    return result


def getfiscalquarter(monthvalue):

    result = ""

    if monthvalue == "06" or monthvalue == "07" or monthvalue == "08":
        result = "Q1"
    if monthvalue == "09" or monthvalue == "10" or monthvalue == "11":
        result = "Q2"
    if monthvalue == "12" or monthvalue == "01" or monthvalue == "02":
        result = "Q3"
    if monthvalue == "03" or monthvalue == "04" or monthvalue == "05":
        result = "Q4"

    return result


def formattedtimestamp(input):

    result = time.strftime("%Y-%m-%d-%H-%M-%S", input)
    return result


def formattedtimestampshort(input):

    result = time.strftime("%Y-%m-%d", input)
    return result


def jiradatetoiso8601(input):

    # This function takes in a Jira date,
    # trims the time portion,
    # and converts to ISO-8601 format.

    # Examples of various Jira dates:
    # 08/Oct/21 12:00 AM
    # 10/8/2021  12:00:00 AM
    # 15/Oct/2021 12:00:00AM +0000

    logging.info(input)
    inputLength = len(input)
    if inputLength == 0:
        input = None
    elif inputLength <= 18:
        input = input[0:9]
        input = datetime.datetime.strptime(input, "%d/%b/%y")
    elif inputLength == 22 or inputLength == 23:
        input = input[0:10]
        input = datetime.datetime.strptime(input, "%m/%d/%Y")
    elif inputLength == 28:
        input = input[0:11]
        input = datetime.datetime.strptime(input, "%d/%b/%Y")

    # input = str(input)
    # result = input[0:10]

    logging.info(input)

    return input
