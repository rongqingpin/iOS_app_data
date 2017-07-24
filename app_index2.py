import urllib
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np

#flc = '/Users/pinqingkan/Desktop/Codes/Project_iTunes/'
#flc = '/Users/Melanie/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Codes/Project_iTunes/'

# load the categories
fname = flc + 'IDs/iosapp_categories.csv'
X = pd.read_csv(fname)
# remove 'games', 'magazines & newspapers', 'stickers'
X = X.drop(labels = [7, 28, 67], axis = 0)

Ncatg, N = X.shape

# old data
fname = flc + 'IDs/iosapp_index.csv'
Y = pd.read_csv(fname)

# record the alphabetical pages of each category
Nalph = 27 # A-Z + *
for icat in range(7, Ncatg):#range(Ncatg):
    alphabets = []
    icategory = X.Category.iloc[icat]
    icatid = X.ID.iloc[icat]

    # old data
    icatapps = Y[Y.ID_category == icatid]
    print(icategory)
    fname = flc + 'isoapp_links/iosapp_' + icategory + '_links_072017.txt'

    link = 'https://itunes.apple.com/us/genre/ios-' + icategory + '/id' + str(icatid) + '?mt=8'
    for ialpha in range(ord('A'), ord('Z')+1):
        ialphabet = link + '&letter=' + chr(ialpha)
        alphabets.append(ialphabet)
    ialphabet = link + '&letter=*'
    alphabets.append(ialphabet)

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

    # compare with old and save the new links
    for link in apps:
        match = re.search('id([\d]+)\?mt', link)
        if match:
            iid = match.group(1)
            iid = int(iid)
            if len(icatapps[icatapps.ID == iid]) < 1: # new data
                # write the new links
                with open(fname, 'a') as txtfile:
                    txtfile.write('%s\n' % link)
                # update the data for app indices
                match = re.search('app/([\w\W]*)/id', link)
                if match:
                    appnew = [[icategory, icatid, match.group(1), iid]]
                    appnew = pd.DataFrame(appnew, columns = Y.columns.values)
                    icatapps = icatapps.append(appnew, ignore_index = True)

    fname = flc + 'IDs/iosapp_' + icategory + '_index.csv'
    icatapps.to_csv(fname, index = False)
