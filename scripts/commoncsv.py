import csv
import logging
import codecs


def loadCscvIntoList(csvPath):

    localList = []
    localList.clear()

    with codecs.open(csvPath, encoding='utf-8', errors='replace') as csvfile:
        try:
            localList = list(csv.DictReader(csvfile))
            result = localList
        except Exception as e:
            logging.critical("Fail: " + csvPath)
            logging.critical("Exception Message: " + repr(e))
            result = None

    # logging.critical(list(localDict.keys()))

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
    except Exception:
        logging.exception('Failed to write to CSV file.')
