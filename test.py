from algorithms import map
import csv

kmeans_predicted_results_file = "data/results/kmeans_predict.csv"
test_results_file = "data/results/kmeans_test.csv"
user_cf_mr_predict_results_file = "data/results/user_cf_mr_predict.csv"
user_cf_mr_test_results_file = "data/results/user_cf_mr_test.csv"

if __name__ == '__main__':

    kmeans_test_results = []
    kmeans_predicted_results = []
    user_cf_mr_predict_results = []
    user_cf_mr_test_results = []

    f = open(kmeans_predicted_results_file, 'rt')
    reader = csv.reader(f)
    for row in reader:
        user = row[0]
        songs = row[1:]
        kmeans_predicted_results.append(songs)
        
    f = open(test_results_file, 'rt')
    reader = csv.reader(f)
    for row in reader:
        user = row[0]
        songs = row[1:]
        kmeans_test_results.append(songs)

    f = open(user_cf_mr_test_results_file, 'rt')
    reader = csv.reader(f)
    for row in reader:
        user = row[0]
        songs = row[1:]
        user_cf_mr_test_results.append(songs)


    f = open(user_cf_mr_predict_results_file, 'rt')
    reader = csv.reader(f)
    for row in reader:
        user = row[0]
        songs = row[1:]
        user_cf_mr_predict_results.append(songs)
    
    # print "kmeans"
    # print map.kdd_mapk(kmeans_test_results, kmeans_predicted_results, 500)

    print "user_cf"
    print map.kdd_mapk(user_cf_mr_test_results, user_cf_mr_predict_results,500)

