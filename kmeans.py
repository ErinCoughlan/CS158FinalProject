from sklearn.cluster import KMeans
from sklearn import preprocessing
import numpy as np
import pdb

def process(data):
    ''' takens in normal array of numerical and categorical attributes
     returns an np array of only numerical values '''

    enc = preprocessing.LabelEncoder()

    # get lists of categories for each attribute
    cat_vals = {}
    for row in data:
        for i, attr in enumerate(row):
            # attr is categorical
            if isinstance(attr,str):
                if cat_vals.get(i,None) is None:
                    cat_vals[i] = [attr]
                else:
                    cat_vals[i].append(attr)

    # encode each list of category values


    # enc.fit(data[1])

    # result = enc.transform(data)

    # print result

    return "result"




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


