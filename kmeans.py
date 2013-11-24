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

def testKmeans(learner, test_data, num_recs):







if __name__ == '__main__':

    # numerical test data
    num_data = np.array([[0.1,0.2,0.3],
                        [0.4,0.5,0.6],
                        [0.7,0.8,0.9]])

    # categorical test data
    data = process([['abc', 0.2, 0.3, 'aou'],
                    ['bge', 0.1, 0.4, 'aou'],
                    ['def', 0.1, 0.3, 'bbb']])
    
    # n_init?
    kmeans = KMeans(init='k-means++', n_clusters=2, n_init=10)

    kmeans.fit(data)

    test = [0.9,0.8,0.9]

    prediction = kmeans.predict(test)

    print prediction


