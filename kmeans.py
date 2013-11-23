from sklearn.cluster import KMeans
import numpy as np

data = np.array([[0.1,0.2,0.3],
								[0.4,0.5,0.6],
								[0.7,0.8,0.9]])

# n_init?
kmeans = KMeans(init='k-means++', n_clusters=2, n_init=10)

kmeans.fit(data)

test = [0.9,0.8,0.9]

prediction = kmeans.predict(test)

print prediction


