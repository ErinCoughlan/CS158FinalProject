from sklearn.cluster import KMeans
from algorithms import map
from collections import Counter
import csv
import numpy as np
import pdb

predicted_results = "data/results/kmeans_predict.csv"
test_results = "data/results/kmeans_test.csv"

def getRecs(learner, num_recs, centroid, song_data_full, song_counts):
    ''' returns the top-n recommendations for a given user's
    centroid based on the learner we give it'''

    cluster = learner.predict(centroid)

    # find all songs in cluster
    cluster_songs = []
    for i, song in enumerate(song_data_full):
        song_id = song[0]
        if learner.labels_[i] == cluster:
            cluster_songs.append(song_id)

    # generate counters of total song counts and cluster song counts
    cluster_song_counts = Counter()
    total_song_counts = Counter()
    for user, songs in song_counts.items():
        for [song,count] in songs:            
            if song in cluster_songs:
                cluster_song_counts[song] += count
            else:
                total_song_counts[song] += count

    # filter and order songs based on play counts
    song_recs = []
    if len(cluster_songs) >= num_recs:
        # if we have enough songs, just use cluster_song_counts
        songs = [song[0] for song in cluster_song_counts.most_common(num_recs)]
        song_recs += songs
    else:
        # if we don't have enough songs, use cluster_song_counts and total_song_counts
        top_n = num_recs - len(cluster_songs)
        cluster_songs = [song[0] for song in cluster_song_counts.most_common(len(cluster_songs))]
        song_recs += cluster_songs
        top_songs = [song[0] for song in total_song_counts.most_common(top_n)]
        song_recs += top_songs

    return song_recs
    

def getCentroid(song_list, song_data):
    ''' returns the centroid coordinates of a given user,
    where we pass in a partial listening history '''

    kmeans = KMeans(init='k-means++', n_clusters=1, n_init=10)

    song_data_dict = {}
    for item in song_data:
        song_data_dict[item[0]] = item[1:]

    num_song_not_found = 0

    song_data_filtered = []
    for [song_id,count] in song_list:
        if song_id in song_data_dict.keys():
            song_data_filtered.append(song_data_dict[song_id])
        else:
            num_song_not_found += 1

    kmeans.fit(song_data_filtered)

    # return centroid coordinates
    return kmeans.cluster_centers_

def writeTestData(user_song_test_data):
    """ Get order lists based on song play count for each user in
    user_song_test_data, and then write to a csv """

    results = []
    for user, songs in user_song_test_data.items():
        test_song_counts = Counter()
        for [song,count] in songs:                        
            test_song_counts[song] += count
        top_songs = [song[0] for song in test_song_counts.most_common(len(list(test_song_counts)))]
        results.append([user] + top_songs)

    with open(test_results, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(results)


def trainKmeans(train_data, num_clusters=100):
    ''' returns a kmeans learner based off of train data '''

    #TODO: experiment with other k-means impl
    kmeans = KMeans(init='k-means++', n_clusters=num_clusters, n_init=10)

    return kmeans.fit(train_data)

def testKmeans(learner, song_data_full, user_song_test_data, user_song_train_data):

    results = []

    # for each user in test data calculate centroid
    for user,song_history in user_song_train_data.items():
        # get the number of songs in test_data, so num_recs is equal
        num_recs = len(user_song_test_data[user])
        # feed centroid into learner and find top n recommendations
        centroid = getCentroid(song_history, song_data_full)
        # get similar songs to centroid and append to results
        results.append([user] + getRecs(learner,num_recs,centroid,song_data_full,user_song_train_data))

    
    # write train and test to file
    with open(predicted_results, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(results)

    writeTestData(user_song_test_data)

    # for each user calculate average precision, and then take mean to get the mAP
    return map.MeanAveragePrecision(test_results, predicted_results)
