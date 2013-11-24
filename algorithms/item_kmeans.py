from sklearn.cluster import KMeans
import numpy as np
import pdb


def getRecs(learner, num_recs, centroid):
    ''' returns the top-n recommendations for a given user's
    centroid based on the learner we give it'''

    pass

def getCentroid(song_list, song_data):
    ''' returns the centroid coordinates of a given user,
    where we pass in a partial listening history '''

    kmeans = KMeans(init='k-means++', n_clusters=1, n_init=10)

    song_data_dict = {}
    for item in song_data:
    	song_data_dict[item[0]] = item[2:]


    num_song_not_found = 0

    song_data_filtered = [[]]
    for [song_id,count] in song_list:
    	if song_id in song_data_dict.keys():
    		song_data_filtered.append(song_data_dict[song_id])
    	else:
    		num_song_not_found += 1

    print "num song not found: ", num_song_not_found

    kmeans.fit(song_data_filtered)

    pdb.set_trace()    		


def trainKmeans(train_data, num_clusters=100):
    ''' returns a kmeans learner based off of train data '''

    #TODO: experiment with other k-means impl
    kmeans = KMeans(init='k-means++', n_clusters=num_clusters, n_init=10)

    return kmeans.fit(train_data)

def testKmeans(learner, song_data, user_song_test_data, user_song_train_data, num_recs=500):

	# for each user in test data calculate centroid
	for user,song_history in user_song_train_data.items():
		getCentroid(song_history, song_data)
		break
	

	# feed centroid into learner and find top n recommendations
	

	# for each user calculate average precision, and then take mean
	# to get the mAP
	

	return "stuff"