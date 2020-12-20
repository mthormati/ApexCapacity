import os.path
import requests
import schedule
import time

from datetime import datetime, timedelta
from properties import *

def main():
    capacity = getCapacity()
    if (capacity >= 0):
        dayTimeTag = getDayTimeTag()
        updateData(dayTimeTag, capacity)

def getCapacity():
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            counters = response.json()['counters']
            for counter in counters:
                if (counter['counter_slug'] == 'climbing-area'):
                    return counter['current_count']
    except Exception as e:
        print(e)
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

if __name__ == '__main__':
    schedule.every().hour.at(':31').do(main)
    schedule.every().hour.at(':01').do(main)
    while True:
        schedule.run_pending()
        time.sleep(60)