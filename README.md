# iOS_app_data
codes for website data scraping and accessing iTunes API on iOS mobile apps

1. run **apps_categories.py**: scrape the categories & IDs of iOS apps ([website link](https://itunes.apple.com/us/genre/ios/id36?mt=8))
2. **websitelinks2_2.py**: compile a complete list of apps for each category (the links on [website link](https://itunes.apple.com/us/genre/ios/id36?mt=8))
3. **app_index2.py**: extract the app names & IDs into DataFrame; compare with previous list for updates
4. **app_data2.py**: access iTunes API; save the app data into csv files. the app features include: info about the developer (ID, website, app store page); ratings (user rating and counts, content rating); app specifics (price, version, release date, genre, size, supported device); app descriptions (descriptions, screen shots, ipad version screen shots)
