import pandas as pd
import csv
import json
import re

# load the category IDs
flc = '/Users/pinqingkan/Desktop/Codes/Project_iTunes/'
#flc = '/Users/Melanie/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Codes/Project_iTunes/'
fname = flc + 'IDs/iosapp_categories.csv'
X0 = pd.read_csv(fname)
# remove repetitive ones: 'games', 'magazines & newspapers', 'stickers'
X0 = X0.drop(labels = [7, 28, 67], axis = 0)

Ncatg, N = X0.shape

# creat a list of desired data
app_keys = ['trackId',
            'artistId',
            'artistViewUrl', 'sellerUrl',
            'contentAdvisoryRating', 'trackContentRating', 'averageUserRating', 'averageUserRatingForCurrentVersion',
            'userRatingCount', 'userRatingCountForCurrentVersion',
            'currency', 'formattedPrice', 'price',
            'currentVersionReleaseDate', 'releaseDate', 'version',
            'genreIds', 'primaryGenreId',
            'fileSizeBytes',
            'screenshotUrls', 'ipadScreenshotUrls',
            'supportedDevices']
Ndict = len(app_keys)
app_keys2 = ['trackId', 'description', 'features']
Nfeat = len(app_keys2)

url0 = 'https://itunes.apple.com/lookup?id='

# loop through the categories
for icat in range(31, 33):#range(33, Ncatg)
    icategory = X0.Category.iloc[icat]
    icatid = X0.ID.iloc[icat]
    # record the data one file per category
    if (icatid >= 7000) & (icatid < 8000): fname0 = 'games'
    elif (icatid >= 13000) & (icatid < 14000): fname0 = 'magazines-newspapers'
    elif icatid >= 16000: fname0 = 'stickers'
    else: fname0 = icategory

    print(icategory)

    # load the new links
    try:
        fname = flc + 'isoapp_links/iosapp_' + icategory + '_links_072017.txt'
        with open(fname, 'r') as file:
            links = file.readlines()

        napp = len(links)
        for iapp in range(napp):
            match = re.search('id([\d]+)\?mt', links[iapp])
            if match:
                iurl = url0 + match.group(1)
                # load data from website
                Y = pd.read_json(iurl)

                # initialize the data
                app_dict = dict.fromkeys(app_keys)
                app_feat = dict.fromkeys(app_keys2)

                if len(Y) > 0:
                    Y = Y['results'][0]

                    # format & record the data
                    for ikey in app_keys:
                        if ikey in Y.keys():
                            if ikey in ['screenshotUrls', 'ipadScreenshotUrls',
                                        'supportedDevices',
                                        'artistViewUrl', 'sellerUrl',
                                        'genreIds']:
                                app_dict[ikey] = len(Y[ikey])
                            elif ikey in ['version']:
                                if len(Y[ikey].encode()) == len(Y[ikey]):
                                    app_dict[ikey] = Y[ikey]
                            else:
                                app_dict[ikey] = Y[ikey]
                        else:
                            app_dict[ikey] = 0

                    # record the description info
                    for ikey in app_keys2:
                        if ikey in Y.keys():
                            app_feat[ikey] = Y[ikey]
                        else:
                            app_feat[ikey] = 0

                # convert into dataframe
                y = pd.DataFrame(app_dict, index = [0])

                # record the app data
                fname = flc + 'iosapp_data/app_data_' + fname0 + '.csv'
                with open(fname, 'a') as file:
                    csvwriter = csv.writer(file, delimiter = '\t')
                    csvwriter.writerow(y.iloc[0,:].values)

                # record the description
                fname = flc + 'iosapp_data/app_descp_' + fname0 + '.json'
                with open(fname, 'a') as file:
                    json.dump(app_feat, file)
                    file.write('\n')

    except FileNotFoundError: continue