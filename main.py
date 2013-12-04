# Erin Coughlan and Evan Casey
# Machine Learning Final Project

from collections import defaultdict
from collections import Counter
import csv
import time
import pdb
import random
import numpy as np

from algorithms import item_kmeans, user_cf
from sklearn import preprocessing
import utils


data_file = "data/kaggle_visible_evaluation_triplets.csv"
data_songs = "data/kaggle_songs.txt"
data_users = "data/kaggle_users.txt"
data_song_track = "data/taste_profile_song_to_tracks.txt"
data_subset_song_track = "data/subset_unique_tracks.txt"
data_analysed_songs = "data/analyzed_data_subset.csv"
#data_analysed_songs = "data/analyzed_data_active_subset.txt"


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

    return data, songCount

def getAnalyzedData():
    """ Grabs the echonest song data and creates a list of lists """

    totalData = []
    f = open(data_analysed_songs, 'rt')
    reader = csv.reader(f)
    for row in reader:
        totalData.append(row)

    return totalData


if __name__ == '__main__':

    # grab user, song data
    user_song_history, songCount = getData()

    # truncate our song data, only run once to generate txt
    # utils.getSmallerSubset(user_song_history,1000)
    # utils.getActiveUserSubset(user_song_history,1000)

    # grab our song data from echonest
    # songDataFull = getAnalyzedData()
    # songDataFull = [item[:-3] for item in songDataFull]

    # user_song_history of first 1000 users
    # user_song_history_subset = utils.truncateDict(user_song_history, 1000)
    user_song_history_subset = truncateDict(user_song_history, 1000)
    # user_song_history of active 1000 users
    #user_song_history_subset = utils.truncateActiveDict(user_song_history, 1000)

    # take out the first index of each sublist (song id)
    # songData = [item[1:] for item in songDataFull]    

    # process the datasets in case of categorical values
    # songData, _ = utils.process(songData)
    
    # for kmeans, take out a random 50% of songs from each user_song_history
    user_song_history_test = {}
    for user,song_list in user_song_history_subset.items():
        user_song_history_test[user] = random.sample(song_list, len(song_list)/2)

    # take out user_song_history_test items from user_song_history
    user_song_history_train = {}
    for user,song_list in user_song_history_test.items():
        user_song_history_train[user] = [song for song in user_song_history_subset[user] if song not in user_song_history_test[user]]

    # songData = np.asarray(songData).astype(np.float)
    # songDataNorm = preprocessing.normalize(songData).tolist()
    # songDataFullNorm = [[songDataFull[i][0]] + songDataNorm[i] for i in range(len(songDataFull))]


    ###### Kmeans ######

    # get our giant kmeans learner
    # kmeans_learner = item_kmeans.trainKmeans(songDataNorm)  

    # item_kmeans.testKmeans(kmeans_learner, songDataFullNorm, user_song_history_test, user_song_history_train)


    ##### User_CF ######
    user_cf.getAllRecommendations(user_song_history_train)


