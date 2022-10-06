import scraper.alt921_scraper as alt921
import spotify.playlist_gen as plg

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # poll the radio station!
    #alt921.alt921_scraper()

    # make a playlist!
    plg.update_playlist("5tBUVqWCyXaSez2b4DolCi", "songs-2022-09-08.csv")
