import urllib
from bs4 import BeautifulSoup
import re
import pandas as pd
from pathlib import Path

# links of the categories
homepage = urllib.request.urlopen('https://itunes.apple.com/us/genre/ios/id36?mt=8')
soup = BeautifulSoup(homepage, 'html5lib')
categories = []
for link in soup.find_all('a'):
    match = re.search(r'https://itunes\.apple\.com/us/genre/ios-[\w\W]+',
                      link.get('href'))
    if match:
        categories.append(match.group())

# id of the categories
pattern = 'ios-([\w-]*)/id([\d]+)'
cats = []
for icategory in categories:
    match = re.search(pattern, icategory)
    if match:
        cats.append([match.group(1), match.group(2)])

# convert to table
X = pd.DataFrame(cats, columns = ['Category', 'ID'])

# check if the categories file already exists
fname = 'iosapp_categories.csv'
file0 = Path(fname)
if file0.is_file(): # if so, check for any difference
    X0 = pd.read_csv(fname)
    diff = np.where(X0 != X)
    if len(sum(diff)) == 0:
        print('same as before')
    else: print(X0.iloc[diff[0], 0])
else:
    X.to_csv('iosapp_categories.csv', index = False) # no such file, then save
