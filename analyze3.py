from collections import defaultdict
from echonest.remix import audio as audio
from pyechonest import config as echoconfig
from pyechonest import track as echotrack
from pyechonest import song as echosong
from pyechonest import util as echoutil
import csv
import pdb

echoconfig.ECHO_NEST_API_KEY = "U98ZZRHBZWNWUDKPW"
data_users_subset = "data/kaggle_users_subset.txt"
data_songs_subset = "data/kaggle_song_subset.txt"
data_song_track = "data/taste_profile_song_to_tracks.txt"


def getData():
    """ Reads in all data files into helpful data structures. """
    uniqueSongs = []
    f = open(data_songs_subset, 'rt')
    reader = csv.reader(f)
    for row in reader:
        song = row[0]
        uniqueSongs.append(song)

    songToTrackFull = {}
    f = open(data_song_track, 'rt')
    reader = csv.reader(f, delimiter="\t")
    for row in reader:
        song = row[0]
        tracks = row[1:]
        if song in uniqueSongs:
            songToTrackFull[song] = tracks

    return uniqueSongs, songToTrackFull

def analyzeTracksNoArtist(songToTrack):
    """ 
        Creates a list of songs for training. Limit allows us to get
        a smaller dataset for testing purposes. Current dataset is based
        on [SongId, Tempo, Danceability, Energy, Speech, Acoutsicness]
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
        if len(data) % 500 == 0:
            count = len(data)
            print "total analyzed: ", count

            with open("data/analyzed_data_subset.txt", "w") as f:
                for d in data:
                    # Convert list to string
                    dString = ""
                    for item in d:
                        dString += str(item) + ','
                    f.write(dString[:-1])
                    f.write('\n')

    return data

if __name__ == '__main__':

    uniqueSongs, songToTrackFull = getData()
    totalData = analyzeTracksNoArtist(songToTrackFull)

    with open("data/analyzed_data_subset.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(totalData)
