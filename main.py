# Erin Coughlan and Evan Casey
# Machine Learning Final Project

from collections import defaultdict
from sklearn.cluster import KMeans
from sklearn import preprocessing
from echonest.remix import audio as audio
from pyechonest import config as echoconfig
from pyechonest import track as echotrack
from pyechonest import song as echosong
from pyechonest import util as echoutil
import numpy as np
import csv
import time

echoconfig.ECHO_NEST_API_KEY = "U98ZZRHBZWNWUDKPW"
data_file = "data/kaggle_visible_evaluation_triplets.txt"
data_songs = "data/kaggle_songs.txt"
data_users = "data/kaggle_users.txt"
data_song_track = "data/taste_profile_song_to_tracks.txt"
data_subset_song_track = "data/subset_unique_tracks.txt"

"""
# Test to determine which data we have access to
songId = songs[0]
trackId, artist, songName = songToTrack[songId]
if trackId != None:
    s = echosong.Song(songId, buckets=['audio_summary'])
    t = echotrack.track_from_id(trackId)
    print s
    artist = s.artist_name
    print artist
    tempo = s.audio_summary["tempo"]
    print tempo
    dance = s.audio_summary["danceability"]
    print dance
    genre = s.song_type
    print genre
"""

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

def process(trainData, testData):
    """ Takes in a normal array of numerical and categorical attributes
     returns an np array of only numerical values """

    # Get lists of categories for each attribute
    catVals = {}
    for row in trainData:
        for i, attr in enumerate(row):
            # attr is categorical
            if isinstance(attr,str):
                if catVals.get(i,None) is None:
                    catVals[i] = [attr]
                else:
                    catVals[i].append(attr)

    for row in testData:
        for i, attr in enumerate(row):
            # attr is categorical
            if isinstance(attr,str):
                if catVals.get(i,None) is None:
                    catVals[i] = [attr]
                else:
                    catVals[i].append(attr)

    # Encode each list of category values
    for cati, values in catVals.items():
        print values
        enc = preprocessing.LabelEncoder()
        enc.fit(values)

        for row in trainData:
            valArr = enc.transform([row[cati]])
            row[cati] = valArr[0]

        for row in testData:
            valArr = enc.transform([row[cati]])
            row[cati] = valArr[0]

    return trainData, testData


if __name__ == '__main__':

    data, songs, users, songToTrack = getData()
    totalData = analyzeTracks(songToTrack, 1000)
    trainData = totalData[0:900]
    testData = totalData[900:]

    """
    # numerical test data
    num_data = np.array([[0.1,0.2,0.3],
                        [0.4,0.5,0.6],
                        [0.7,0.8,0.9]])

    # categorical test data
    train = [['def', 0.2, 0.3, 'aou'],
            ['bge', 0.1, 0.4, 'aou'],
            ['abc', 0.1, 0.3, 'bbb']]

    # NEED TO CONVERT TEST TO SAME NUMERICAL LABELS
    test = [['abc', 0.2, 0.3, 'aou']]

    train, test = process(train, test)
    """

    train, test = process(trainData, testData)
    
    kmeans = KMeans(init='k-means++', n_clusters=100, n_init=10)

    kmeans.fit(train)
    
    prediction = kmeans.predict(test)

    print prediction