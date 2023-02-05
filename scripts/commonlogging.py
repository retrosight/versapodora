import logging
import time

import commondatetime

commonLocalDev = True

def main(logfilename, loglevel, localDev):
    logging.info('common.py - main')

    # Setup logging
    if (not setup_logging(logfilename, loglevel, localDev)):
        print("Failed to setup logging, aborting.")
        return 1


def setup_logging(logfilename, loglevel, localDev):

    logging.info('common.py - setup_logging')

    # normal = Write logs to a permanent file name.
    # timestamped = Write logs to a timestamped file name.
    logfilenameoption = "normal"

    result = True

    if logfilenameoption == "timestamped":
        log_date = commondatetime.formattedtimestamp(time.localtime())
        logfilename = log_date + '-' + logfilename

    logPath = "../resources/logs/"

    if localDev is True or commonLocalDev is True:
        logPath = "../local/logs/"

    log_line_template = "%(asctime)s | %(threadName)-12.12s| %(levelname)-9.9s | %(message)s"

    logFormatter = logging.Formatter(log_line_template)

    logger = logging.getLogger()

    if (logger.hasHandlers()):
        logger.handlers.clear()

    # https://docs.python.org/3/library/logging.html
    logger.setLevel(logging.CRITICAL)

    if (loglevel == 'ERROR'):
        logger.setLevel(logging.ERROR)

    if (loglevel == 'WARNING'):
        logger.setLevel(logging.WARNING)

    if (loglevel == 'INFO'):
        logger.setLevel(logging.INFO)

    if (loglevel == 'DEBUG'):
        logger.setLevel(logging.DEBUG)

    # File Handler

    try:
        with open(logPath + logfilename + ".log", 'w') as f:
            f.write("")
            f.close()
        fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, logfilename))
        fileHandler.setFormatter(logFormatter)
        logger.addHandler(fileHandler)
    except OSError as err:
        logging.exception("common.py - OS error: {0}".format(err))
        result = False

    # Stream Handler

    try:
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        logger.addHandler(consoleHandler)
    except OSError as err:
        logging.exception("common.py - OS error: {0}".format(err))
        result = False

    # Success
    if (result is False):
        return False
    else:
        return True