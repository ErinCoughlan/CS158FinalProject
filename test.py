from algorithms import map
import csv

kmeans_predicted_results_file = "data/results/kmeans_predict.csv"
test_results_file = "data/results/kmeans_test.csv"
user_cf_predicted_results_file = "data/results/user_cf_predict.csv"

if __name__ == '__main__':

    test_results = []
    kmeans_predicted_results = []
    user_cf_predicted_results = []

    f = open(kmeans_predicted_results_file, 'rt')
    reader = csv.reader(f)
    for row in reader:
        user = row[0]
        songs = row[1:]
        kmeans_predicted_results.append(songs)

    """
    f = open(user_cf_predicted_results_file, 'rt')
    reader = csv.reader(f)
    for row in reader:
        user = row[0]
        songs = row[1:]
        user_cf_redicted_results.append(songs)
    """
    
    f = open(test_results_file, 'rt')
    reader = csv.reader(f)
    for row in reader:
        user = row[0]
        songs = row[1:]
        test_results.append(songs)
    
    print "kmeans"
    print map.kdd_mapk(test_results, kmeans_predicted_results, 500)

    print "user_cf"
    #print map.kdd_mapk(test_results, user_cf_predicted_results)

