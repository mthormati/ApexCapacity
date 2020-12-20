import requests
import schedule
import time

from datetime import datetime, timedelta
from properties import *

def updateData():
    capacity = getCapacity()
    if (capacity >= 0):
        print(capacity)
        # print(getTimeBucket())

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

if __name__ == '__main__':
    print(getDayTimeTag())
    # schedule.every().hour.at(':31').do(updateData)
    # schedule.every().hour.at(':01').do(updateData)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)