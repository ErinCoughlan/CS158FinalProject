from sklearn import preprocessing
from collections import defaultdict
from collections import Counter
from algorithms import item_kmeans, user_cf
import random
import csv
import pdb

data_file = "data/kaggle_visible_evaluation_triplets.txt"
train_results = "data/results/user_cf_mr_train.csv"
predicted_results = "data/results/user_cf_mr_predict.csv"
test_results = "data/results/user_cf_mr_test.csv"

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

def getSmallerSubset(user_song_history, num):    
    """ takes in user_song_history and writes a subset of it to .txt"""

    # list of lists of first 1000 users
    uf = user_song_history.values()[:num]
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

def getActiveUserSubset(user_song_history, num):
    """ Creates a subset of the num most active users, meaning most songs
        listened to """

    # Get a list of users and the number of songs listened to
    counts = []
    for user, songList in user_song_history.items():
        counts.append([len(songList), user])

    # Sort and reverse so highest are first
    counts.sort()
    counts.reverse()

    # Get a list of the most active users
    users = [u for [c, u] in counts[:num]]

    # Get the song data for the users
    uf = [user_song_history[u] for u in users]
    # get rid of nested list
    ufx = [x for y in uf for x in y]
    # get just the songs
    ufy = [u[0] for u in ufx]
    #get rid of duplicates
    ufs = list(set(ufy))
    # ufs = [[u] for u in ufs]

    with open("data/kaggle_song_active_subset.txt", "w") as text_file:
        for uid in ufs:
            text_file.write(uid)
            text_file.write('\n')

    with open("data/kaggle_user_active_subset.txt", "w") as text_file:
        for uid in users:
            text_file.write(uid)
            text_file.write('\n')


def truncateActiveDict(user_song_history, num):
    """ user_song_history to a subset of num entries using active users"""

    # Get a list of users and the number of songs listened to
    counts = []
    for user, songList in user_song_history.items():
        counts.append([len(songList), user])

    # Sort and reverse so highest are first
    counts.sort()
    counts.reverse()
    # Get a list of the most active users
    ufkeys = [u for [c, u] in counts[:num]]

    user_song_history_subset = {}
    for key in ufkeys:
        user_song_history_subset[key] = user_song_history[key]

    return user_song_history_subset

def truncateDict(user_song_history, num):
    """ user_song_history to a subset of num entries """

    ufkeys = user_song_history.keys()[:num]
    user_song_history_subset = {}
    for key in ufkeys:
        user_song_history_subset[key] = user_song_history[key]

    return user_song_history_subset

def process(trainData, testData = [[]]):
    """ Takes in a normal array of numerical and categorical attributes
     returns an np array of only numerical values """

    # get lists of categories for each attribute
    catVals = {}
    for row in trainData:
        for i, attr in enumerate(row):
            # attr is categorical
            if isinstance(attr,str):
                if catVals.get(i,None) is None:
                    catVals[i] = [attr]
                else:
                    catVals[i].append(attr)

    # do same for test data
    for row in testData:
        for i, attr in enumerate(row):
            # attr is categorical
            if isinstance(attr,str):
                if catVals.get(i,None) is None:
                    catVals[i] = [attr]
                else:
                    catVals[i].append(attr)

    # encode each list of category values
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


def writeTrainData(user_song_train_data):
    """ Get order lists based on song play count for each user in
    user_song_test_data, and then write to a csv """

    results = user_song_train_data
    with open(train_results, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(results)

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


if __name__ == '__main__':

    # grab user, song data
    user_song_history, songCount = getData()

    user_song_history_subset = truncateDict(user_song_history, 10000)

    user_song_history_test = {}
    for user,song_list in user_song_history_subset.items():
        user_song_history_test[user] = random.sample(song_list, len(song_list)/2)

    # take out user_song_history_test items from user_song_history
    user_song_history_train = []
    for user,song_list in user_song_history_subset.items():
        for song in song_list:            
            if song not in user_song_history_test[user]:
                user_song_history_train.append([user] + song)
             

    user_song_history_train_dict = {}
    for user,song_list in user_song_history_test.items():
        user_song_history_train_dict[user] = [song for song in user_song_history_subset[user] if song not in user_song_history_test[user]]

    writeTestData(user_song_history_test)
    writeTrainData(user_song_history_train)

    user_cf.getAllRecommendations(user_song_history_train_dict)  

