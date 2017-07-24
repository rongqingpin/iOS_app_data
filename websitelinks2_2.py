import urllib
from bs4 import BeautifulSoup
import re
import pandas as pd

# load the categories
fname = '/Users/pinqingkan/Desktop/Codes/Project_iTunes/IDs/iosapp_categories.csv'
X = pd.read_csv(fname)
# remove 'games', 'magazines & newspapers', 'stickers'
X = X.drop(labels = [7, 28, 67], axis = 0)

Ncatg, N = X.shape

# record the alphabetical pages of each category
Nalph = 27 # A-Z + *
for icat in range(1):#range(Ncatg):
    alphabets = []
    icategory = X.Category[icat]
    icatid = X.ID[icat]
    link = 'https://itunes.apple.com/us/genre/ios-' + icategory + '/id' + str(icatid) + '?mt=8'
    for ialpha in range(ord('A'), ord('Z')+1):
        ialphabet = link + '&letter=' + chr(ialpha)
        alphabets.append(ialphabet)
    ialphabet = link + '&letter=*'
    alphabets.append(ialphabet)

    print(icategory)

    # record the pages of each alphabet and compile
    pages = []
    for link0 in alphabets:
        pattern = re.sub(r'\.', '\\.', link0) # inhibit special characters
        pattern = re.sub(r'\?', '\\?', pattern)
        pattern = re.sub(r'\*', '\\*', pattern)
        pattern = pattern + '&[\w\W]+' # pattern of the links
        # go through the links of this alphabet
        ialphabet = urllib.request.urlopen(link0)
        soup = BeautifulSoup(ialphabet, 'html5lib')
        pages0 = []
        for link in soup.find_all('a'):
            match = re.search(pattern, link.get('href'))
            if match:
                pages0.append(match.group())
        if len(pages0) == 0: pages0 = [link0] # if no pages, just record original
        else: pages0 = list(set(pages0)) # remove duplicates
        pages += pages0

    # go through the pages to record the apps
    Npag = len(pages)
    apps = []
    app_link = 'https://itunes\.apple\.com/us/app/' + '[\w\W]+' + '\?mt=8'
    for link0 in pages:
        ipage = urllib.request.urlopen(link0)
        soup = BeautifulSoup(ipage, 'html5lib')
        for link in soup.find_all('a'):
            match = re.search(app_link, link.get('href'))
            if match:
                apps.append(match.group())

    # save the links
    fname = 'iosapp_' + icategory + '_links.txt'
    with open(fname, 'w') as txtfile:
        for link in apps:
            txtfile.write('%s\n' % link)