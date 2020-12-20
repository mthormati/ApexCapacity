import requests
from properties import *

response = requests.get(URL)
if response.status_code == 200:
    print(response.text)