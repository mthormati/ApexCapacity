import logging
import logging.handlers
import os
import requests
import schedule
import time

from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler
from properties import *

logger = logging.getLogger('capacity app logger')

def main():
    logger.info(str(datetime.now()) + ' Starting ')
    capacity = getCapacity()
    logger.info('Capacity: ' + str(capacity))
    if (capacity >= 0):
        dayTimeTag = getDayTimeTag()
        updateData(dayTimeTag, capacity)
    logger.info(str(datetime.now()) + ' Finished')

def getCapacity():
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            counters = response.json()['counters']
            for counter in counters:
                if (counter['counter_slug'] == 'climbing-area'):
                    return counter['current_count']
    except Exception as e:
        logger.error('Exception: ' + str(e))
    return -1

def getDayTimeTag():
    # Day of week, where Monday is 0 and Sunday is 6
    dayOfWeek = datetime.today().weekday()
    # Round down to nearest 30 minute interval
    now = datetime.now()
    timeBucket = str(now - (now - datetime.min) % timedelta(minutes=30)).split(' ')[1]
    return str(dayOfWeek) + ' ' + str(timeBucket)

# Data represented in following format:
# <day of week> <time> <number of data points> <total capacity> <running average> <latest capacity>
# Example: 1 00:30 5 6
def updateData(timeTag: str, capacity: int):
    logger.info('Timetag: ' + timeTag)
    data = []
    if os.path.isfile(datafilePath):
        with open(datafilePath, 'r') as file:
            data = file.readlines()
    updated = False
    for i in range(len(data)):
        if timeTag in data[i]:
            count = int(data[i].split(' ')[2]) + 1
            totalCapacity = int(data[i].split(' ')[3]) + capacity
            averageCapacity = float(totalCapacity) / count
            data[i] = timeTag + ' ' \
                    + str(count) + ' ' \
                    + str(totalCapacity) + ' ' \
                    + str(averageCapacity) + ' ' \
                    + str(capacity) + '\n'
            updated = True
    if not updated:
        data.append(timeTag + ' 1 ' \
                + str(capacity) + ' ' \
                + str(capacity) + ' ' \
                + str(capacity) + '\n')
    with open(datafilePath, 'w') as file:
        file.writelines(data)

def setupLogging():
    if not os.path.isdir(logFileDir):
        os.makedirs(logFileDir)
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(filename=logFilePath, maxBytes=logFileMaxBytes, backupCount=10)
    logger.addHandler(handler)

if __name__ == '__main__':
    setupLogging()
    schedule.every(10).minutes.do(main)
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            logger.error('Exception: ' + str(e))
