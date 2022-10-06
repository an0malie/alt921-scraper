# Alt 92.1 Web Scraper

import datetime
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup


def print_current_song(url, _df):
    xml = requests.get(url).content
    soup = BeautifulSoup(xml, 'xml')

    artist = soup.find('artist').text
    title = soup.find('title').text
    start_time = soup.find('programStartTS').text

    prev_entry = _df['startTime'].str.contains(start_time).any()
    #print(str(datetime.datetime.now()) + ' -> ' + artist.ljust(25) + ' - \t' + title.ljust(25) + '\t\t\tstarted at ' + start_time)
    #print(prev_entry)

    if ~prev_entry:
        data = pd.DataFrame({'artist': [artist], 'title': [title], 'startTime': [start_time]})
        return pd.DataFrame(data)
    #else:
        #print('duplicate entry')


def alt921_scraper():
    url = 'https://streamdb6web.securenetsystems.net/player_status_update/ALT921.xml'
    cols = {'artist': pd.Series(dtype='str'), 'title': pd.Series(dtype='str'), 'startTime': pd.Series(dtype='str')}
    df = pd.DataFrame(columns=cols)
    today = datetime.date.today()
    count = 0

    # run for a full day (24 hrs / 100 second poll)
    while count < 864:
        df = pd.concat([df, print_current_song(url, df)], ignore_index=True)
        count += 1
        print(df)
        if count % 10 == 0:
            df.to_csv('songs-' + str(today) + '.csv', index=False)
        time.sleep(100)

    df.to_csv('songs-' + str(today) + '.csv', index=False)
