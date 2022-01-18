import requests
from bs4 import BeautifulSoup

while True:
    r = requests.get('https://www.youtube.com/c/SimpleCodeIT/videos').text
    bs = BeautifulSoup(r)
    print(bs)
    break