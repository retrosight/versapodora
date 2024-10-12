import csv
import logging
import codecs


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

    return result


def writeArrayToCsv(fields, data, filename):
    logging.info('writeArrayToCsv')
    localPath = "../local/output/"

    try:
        csvDataPath = localPath + filename
        with open(csvDataPath, mode='w') as csv_file:
            csvWriter = csv.DictWriter(csv_file, fieldnames=fields)
            csvWriter.writeheader()
            for row in data:
                csvWriter.writerow(row)
            logging.critical("Success writing to: " + csvDataPath)
    except Exception:
        logging.exception('Failed to write to CSV file.')
