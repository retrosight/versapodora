import csv
import logging
import codecs


def loadCscvIntoArray(csvPath):

    localDict = []
    localDict.clear()

    with codecs.open(csvPath, encoding='utf-8', errors='replace') as csvfile:
        localDict = list(csv.DictReader(csvfile))

    # logging.critical(list(localDict.keys()))

    return localDict


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
