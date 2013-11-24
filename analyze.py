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
    songToTrack = {}
    f = open(data_subset_song_track, 'rt')
    reader = csv.reader(f)
    for row in reader:
        row = row[0].split('<SEP>')
        track, song, artist, songName = row
        songToTrack[song] = [track, artist, songName]

    songToTrackFull = {}
    f = open(data_song_track, 'rt')
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        song = row[0]
        tracks = row[1:]
        songToTrackFull[song] = tracks

    return songToTrack, songToTrackFull


def analyzeTracks(songToTrack):
    """ 
        Creates a list of songs for training. Limit allows us to get
        a smaller dataset for testing purposes. Current dataset is based
        on [Artist, Tempo, Danceability, Energy, Speech, Acoustic]
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

    return data

def analyzeTracksNoArtist(songToTrack):
    """ 
        Creates a list of songs for training. Limit allows us to get
        a smaller dataset for testing purposes. Current dataset is based
        on [Tempo, Danceability, Energy]
    """

    data = []
    for song, trackIds in songToTrack.items():
        if len(trackIds) == 0: continue
        trackId = trackIds[0]
        while True:
            try:
                t = echotrack.track_from_id(trackId)
                t.get_analysis()
                tempo = t.tempo
                dance = t.danceability
                energy = t.energy
                speech = t.speechiness
                acoustic = t.acousticness
                data.append([song, tempo, dance, energy, speech, acoustic])
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
            with open("data/analyzed_data.csv", "wb") as f:
                writer = csv.writer(f)
                writer.writerows(data)

    return data

if __name__ == '__main__':

    songToTrack, songToTrackFull = getData()
    #totalData = analyzeTracks(songToTrack)
    totalData = analyzeTracksNoArtist(songToTrackFull)

    with open("data/analyzed_data.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(totalData)
