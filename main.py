# Erin Coughlan and Evan Casey
# Machine Learning Final Project

from collections import defaultdict
from collections import Counter
from sklearn import preprocessing
from echonest.remix import audio as audio
from pyechonest import config as echoconfig
from pyechonest import track as echotrack
from pyechonest import song as echosong
from pyechonest import util as echoutil
import numpy as np
import csv
import time
import random
from algorithms import item_kmeans, user_cf
import pdb
import random

echoconfig.ECHO_NEST_API_KEY = "U98ZZRHBZWNWUDKPW"
data_file = "data/kaggle_visible_evaluation_triplets.txt"
data_songs = "data/kaggle_songs.txt"
data_users = "data/kaggle_users.txt"
data_song_track = "data/taste_profile_song_to_tracks.txt"
data_subset_song_track = "data/subset_unique_tracks.txt"
data_analysed_songs = "data/analyzed_data_2.csv" #TODO fix this


def getData():
    """ Reads in all data files into helpful data structures. """
    data = {}
    data = defaultdict(list)
    songCount = Counter()
    f = open(data_file, 'rt')
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        user = row[0]
        song = row[1]
        count = int(row[2])
        data[user].append([song, count])
        songCount[song] += count

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

    return data, songs, users, songToTrack, songCount

def getAnalyzedData():
    totalData = []
    f = open(data_analysed_songs, 'rt')
    reader = csv.reader(f)
    for row in reader:
        totalData.append(row)

    return totalData

def process(trainData, testData = [[]]):
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
        enc = preprocessing.LabelEncoder()
        enc.fit(values)

        for row in trainData:
            if cati < len(row)-1: 
                valArr = enc.transform([row[cati]])
                row[cati] = valArr[0]

        for row in testData:
            if cati < len(row)-1: 
                valArr = enc.transform([row[cati]])
                row[cati] = valArr[0]

    return trainData, testData

def getSmallerSubset(user_song_history):    

    # list of lists of first 1000 users
    uf = user_song_history.values()[:1000]
    # get rid of nested list
    ufx = [x for y in uf for x in y]
    # get just the songs
    ufy = [u[0] for u in ufx]
    #get rid of duplicates
    ufs = list(set(ufy))
    # ufs = [[u] for u in ufs]
     
    with open("data/kaggle_song_subset.txt", "w") as text_file:
        for uid in ufs:
            text_file.write(uid)
            text_file.write('\n')


if __name__ == '__main__':

    # grab song data
    user_song_history, songs, users, songToTrack, songCount = getData()

    # truncate our song data, only run once to generate txt
    getSmallerSubset(user_song_history)

    songDataFull = getAnalyzedData()

    # user_song_history of first 1000 users
    ufkeys = user_song_history.keys()[:1000]
    user_song_history_subset = {}
    for key in ufkeys:
        user_song_history_subset[key] = user_song_history[key]

    # take out the first index of each sublist
    # get rid of artist too
    songData = [item[2:] for item in songDataFull]    

    # process the datasets in case of categorical values
    songData, _ = process(songData)
    
    # for kmeans, take out a random 50% of songs from each user_song_history
    user_song_history_test = {}
    for user,song_list in user_song_history_subset.items():
        user_song_history_test[user] = random.sample(song_list, len(song_list)/2)

    # take out user_song_history_test items from user_song_history
    user_song_history_train = {}
    for user,song_list in user_song_history_test.items():
        user_song_history_train[user] = [song for song in user_song_history_subset[user] if song not in user_song_history_test[user]]

    # get our giant kmeans learner
    kmeans_learner = item_kmeans.trainKmeans(songData)  

    # 
    kmeans_results = item_kmeans.testKmeans(kmeans_learner, songDataFull, user_song_history_test, user_song_history_train)