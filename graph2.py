# Actual do the graphing
# Erin Coughlan and Evan Casey

import matplotlib.pyplot as plt
import csv
import numpy as np

# Get the results from file
f = open("data/results/graph.txt", 'rt')
data = []
reader = csv.reader(f)
for row in reader:
	data.append(row)

[clusters, results] = data

clusters = [float(c) for c in clusters]
results = [float(r) for r in results]

# Quadratic fit
coefficients = np.polyfit(clusters, results, 3)
polynomial = np.poly1d(coefficients)
xs = range(500)
ys = polynomial(xs)

plt.ylabel('Accuracy')
plt.xlabel('Number of Clusters')

plt.plot(clusters, results, 'ro')
plt.plot(xs, ys)
plt.show()
