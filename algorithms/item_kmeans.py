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


def trainKmeans(train_data, num_clusters):
    ''' returns a kmeans learner based off of train data '''
    pass

def testKmeans(learner, test_data, num_recs):
	pass