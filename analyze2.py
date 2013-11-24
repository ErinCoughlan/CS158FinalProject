from collections import defaultdict
from echonest.remix import audio as audio
from pyechonest import config as echoconfig
from pyechonest import track as echotrack
from pyechonest import song as echosong
from pyechonest import util as echoutil
import csv

echoconfig.ECHO_NEST_API_KEY = "U98ZZRHBZWNWUDKPW"
data_file = "data/kaggle_visible_evaluation_triplets.txt"
data_songs = "data/kaggle_songs.txt"
data_users = "data/kaggle_users.txt"
data_song_track = "data/taste_profile_song_to_tracks.txt"
data_subset_song_track = "data/subset_unique_tracks.txt"


def getData():
    """ Reads in all data files into helpful data structures. """
    data = {}
    data = defaultdict(list)
    f = open(data_file, 'rt')
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        user = row[0]
        data[user].append(row[1:])

    songs = []
    f = open(data_songs, 'rt')
    reader = csv.reader(f, delimiter=' ')
    for row in reader:
        song = row[0]
        songs.append(song)

    users = []
    f = open(data_users, 'rt')
    reader = csv.reader(f)
    for row in reader:
        users.append(row)

    songToTrack = {}
    f = open(data_subset_song_track, 'rt')
    reader = csv.reader(f)
    for row in reader:
        row = row[0].split('<SEP>')
        track, song, artist, songName = row
        songToTrack[song] = [track, artist, songName]

    return data, songs, users, songToTrack


def analyzeTracks(songToTrack):
    """ 
        Creates a list of songs for training. Limit allows us to get
        a smaller dataset for testing purposes. Current dataset is based
        on [Artist, Tempo, Danceability, Energy]
    """

    data = []
    for song, trackInfo in songToTrack.items():
        trackId, artist, songName = trackInfo
        while True:
            try:
                t = echotrack.track_from_id(trackId)
                t.get_analysis()
                tempo = t.tempo
                dance = t.danceability
                energy = t.energy
                speech = t.speechiness
                acoustic = t.acousticness
                data.append([song, artist, tempo, dance, energy, speech, acoustic])
            except echoutil.EchoNestAPIError: # We exceeded our access limit
                print "too many accesses per minute - retry in a minute"
                time.sleep(60)
                continue
            except IndexError: # The song wasn't found on echo nest
                print "index error - skip"
                break
            except echoutil.EchoNestIOError: # Unknown error from echo nest
                print "unknown error - retry"
                continue
            break # retry request

        # Write to file every 1000 analyzes 
        if len(data) % 1000 == 0:
            with open("data/analyzed_data_2.csv", "wb") as f:
                writer = csv.writer(f)
                writer.writerows(data)

    return data

if __name__ == '__main__':

    data, songs, users, songToTrack = getData()
    totalData = analyzeTracks(songToTrack)

    with open("data/analyzed_data_2.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(totalData)
