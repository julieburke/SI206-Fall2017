import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re

address = ' http://py4e-data.dr-chuck.net/known_by_Colton.html'


n = 0
x = 0
while n < 7:
    html = urllib.request.urlopen(address).read()
    soup = BeautifulSoup(html)
    tags = soup('a')
    
    for link in tags:
        x = x + 1
        if x == 18:
            address = link.get('href', None)

            x = 0
            break
    n = n + 1

print (address)