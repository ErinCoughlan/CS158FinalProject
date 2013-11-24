from sklearn.cluster import KMeans
import numpy as np
import pdb


def getRecs(learner, num_recs, centroid):
    ''' returns the top-n recommendations for a given user's
    centroid based on the learner we give it'''

    pass

def getCentroid(user_history):
    ''' returns the centroid coordinates of a given user,
    where we pass in a partial listening history '''

    pass


def trainKmeans(train_data, num_clusters=100):
    ''' returns a kmeans learner based off of train data '''
    pass

def testKmeans(learner, user_song_test_data, user_song_train_data, num_recs=500):

	# for each user in test data calculate centroid
	

	# feed centroid into learner and find top n recommendations
	

	# for each user calculate average precision, and then take mean
	# to get the mAP
	

	pass