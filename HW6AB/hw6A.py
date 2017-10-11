import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re

url = 'http://py4e-data.dr-chuck.net/comments_31748.html'
html = urllib.request.urlopen(url).read()
totsum = 0
soup = BeautifulSoup(html, 'html.parser')
tags = soup('span')
for tag in tags:
	for item in re.findall("([0-9]+)", str(tag)):

		totsum += int(item)
print (totsum)