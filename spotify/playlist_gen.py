import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotify.config import APP_CLIENT_ID, APP_CLIENT_SECRET


def init_spotipy():
    auth_manager = SpotifyOAuth(
        scope="playlist-modify-public",
        redirect_uri='http://127.0.0.1:9090',
        client_id=APP_CLIENT_ID,
        client_secret=APP_CLIENT_SECRET,
        cache_path="token.txt"
    )
    #return spotipy.Spotify(auth=auth_manager)
    return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=APP_CLIENT_ID,
        client_secret=APP_CLIENT_SECRET, redirect_uri='http://127.0.0.1:9090', scope="playlist-modify-private"))


def clean_artist(artist):
    if artist == 'PANIC! AT THE DISCO':
        return 'PANIC AT THE DISCO'
    elif artist == 'ARTIC MONKEYS':
        return 'ARCTIC MONKEYS'
    elif artist == 'GOTYE (GOH-TEE-AY)':
        return 'GOTYE'
    elif artist == 'MARSHMELLO FEATURING BASTILLE':
        return 'MARSHMELLO BASTILLE'
    elif artist == '30 SECONDS TO MARS':
        return 'THIRTY SECONDS TO MARS'
    elif artist == 'SUCH GREAT HEIGHTS':
        return 'THE POSTAL SERVICE'
    elif artist == 'HEAD AND THE HEART':
        return 'THE HEAD AND THE HEART'
    elif artist == 'COLDPLAY':
        return 'c0ldpl@y' # I HATE COLDPLAY!!

    return artist


def clean_title(title):
    if title == 'RAMONE AYALA':
        return 'RAMON AYALA'
    elif title == 'SUGAR, WE\'RE GOING DOWN':
        return 'SUGAR, WE\'RE GOIN DOWN'
    elif title == 'FALLING WITH ME':
        return 'FALLIN WITH ME'
    elif title == 'FIRST TIME':
        return '1ST TIME'
    elif title == 'MISSED CONNECTIONS':
        return 'MISSED CONNECTION'

    return title.translate({ord(c): None for c in '\'!@#$'})


def clean_data(_artist, _title):
    if _artist == 'SIT NEXT TO ME' and _title == 'FOSTER THE PEOPLE':
        _artist = 'FOSTER THE PEOPLE'
        _title = 'SIT NEXT TO ME'
    elif _artist == 'MONSTERS FEAT. BLACKBEAR' and _title == 'ALL TIME LOW':
        _artist = 'ALL TIME LOW'
        _title = 'MONSTERS'
    elif _artist == 'YOUNG BLOOD' and _title == 'NAKED AND FAMOUS':
        _artist = 'NAKED AND FAMOUS'
        _title = 'YOUNG BLOOD'

    artist = clean_artist(_artist)
    title = clean_title(_title)

    return artist, title


def update_playlist(playlist_name, filename):
    sp = init_spotipy()

    df = pd.read_csv(filename)
    df = df.drop_duplicates(subset=['artist', 'title'], keep='first')

    track_ids = []
    unknown_tracks = []

    tracks = zip(df['artist'], df['title'])
    count = 1
    num_tracks = len(df)

    for track in tracks:
        artist, title = clean_data(track[0], track[1])

        results = sp.search(q='artist:' + artist + ' track:' + title, limit=1, type='track')

        if len(results['tracks']['items']) == 1:
            track_ids.append(results['tracks']['items'][0]['id'])
            print('found track ' + str(count) + ' of ' + str(num_tracks))
        else:
            unknown_tracks.append(track)
            print('error finding track ' + str(count) + ' of ' + str(num_tracks))

        count += 1

    print('IDs!!!!!')
    print(track_ids)

    print('COULDNT FIND!!!')
    print(unknown_tracks)

    if len(track_ids) > 100:
        sp.playlist_replace_items(playlist_name, track_ids[:100])
        loops = int(len(track_ids)/100)
        for i in range(loops):
            sp.playlist_add_items(playlist_name, track_ids[((i+1)*100):((i+1)*100+100)])
