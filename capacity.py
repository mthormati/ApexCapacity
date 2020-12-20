import requests
from properties import *


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

if __name__ == '__main__':
    capacity = getCapacity()
    print(capacity)