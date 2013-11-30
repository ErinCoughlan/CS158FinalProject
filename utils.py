from sklearn import preprocessing

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