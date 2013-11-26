#!/usr/bin/env python
# https://gist.github.com/rsivapr/2976729
 
import sys
import csv
 
def MeanAveragePrecision(valid_filename, attempt_filename, at=10):
    at = int(at)
    valid = dict()
    for line in csv.DictReader(open(valid_filename,'r')):
        valid.setdefault(line['source_node'],set()).update(line['destination_nodes'].split(" "))
    attempt = list()
    for line in csv.DictReader(open(attempt_filename,'r')):
        attempt.append([line['source_node'], line['destination_nodes'].split(" ")])
    average_precisions = list()
    for entry in attempt:
        node = entry[0]
        predictions = entry[1]
        correct = list(valid.get(node,dict()))
        total_correct = len(correct)
        if len(predictions) == 0 or total_correct == 0:
            average_precisions.append(0)
            continue
        running_correct_count = 0
        running_score = 0
        for i in range(min(len(predictions),at)):
            if predictions[i] in correct:
                correct.remove(predictions[i])
                running_correct_count += 1
                running_score += float(running_correct_count) / (i+1)
        average_precisions.append(running_score / min(total_correct, at))
    return sum(average_precisions) / len(average_precisions)
 
if __name__ == "__main__":
    if len(sys.argv) == 3:
        print MeanAveragePrecision(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4:
        print MeanAveragePrecision(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print "args: valid.csv attempt.csv [10]"