import csv
import logging
import codecs
import traceback


def loadCscvIntoList(csvPath):

    localList = []
    localList.clear()

    result = None

    try:
        with codecs.open(csvPath, encoding='utf-8', errors='replace') as csvfile:
            try:
                localList = list(csv.DictReader(csvfile))
                result = localList
            except Exception as e:
                logging.critical("Fail: " + csvPath)
                logging.critical("Exception Message: " + repr(e))
    except IsADirectoryError as e:
        logging.info("This is a folder.")
        result = "Folder"
    except Exception as e:
        logging.critical("Exception Message: " + repr(e))
        logging.critical("Path: " + csvPath)

    return result


def writeArrayToCsv(fields, data, filepath):

    try:
        with open(filepath, mode='w') as csv_file:
            csvWriter = csv.DictWriter(csv_file, fieldnames=fields)
            csvWriter.writeheader()
            for row in data:
                csvWriter.writerow(row)
            logging.critical("Success writing CSV to: " + filepath)
    except Exception as e:
        logging.critical('Exception handled. Stack trace is as follows:')
        logging.critical(traceback.print_exc())
