from algorithms import map
import csv

predicted_results_file = "data/results/kmeans_predict.csv"
test_results_file = "data/results/kmeans_test.csv"

if __name__ == '__main__':

    test_results = []
    predicted_results = []

    f = open(predicted_results_file, 'rt')
    reader = csv.reader(f)
    for row in reader:
        user = row[0]
        songs = row[1:]
        predicted_results.append(songs)
    
    f = open(test_results_file, 'rt')
    reader = csv.reader(f)
    for row in reader:
        user = row[0]
        songs = row[1:]
        test_results.append(songs)
    
    
    print map.kdd_mapk(test_results, predicted_results)