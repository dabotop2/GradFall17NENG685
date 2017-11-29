# -*- coding: utf-8 -*-
"""
NENG685 Final Project
DBSCAN
@author: Kevin Choe
"""
from DBSCAN_data import Data_array as X
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
# #############################################################################

centers = [[1, 1], [-1, -1], [1, -1]]

# #############################################################################

# Compute DBSCAN
db = DBSCAN(eps=0.3, min_samples=6).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
print('Estimated number of clusters: %d (eps=.3; min=6)' % n_clusters_)

# #############################################################################
# Original plot to show that Boundary circles < Core circles

unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    if k == -1:
       col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

    Clusters = X[class_member_mask & core_samples_mask]
    plt.plot(Clusters[:, 0], Clusters[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=14)

    Outliers = X[class_member_mask & ~core_samples_mask]
    plt.plot(Outliers[:, 0], Outliers[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=6)

plt.xlim([-5,4])
plt.ylim([-5,5])
plt.title('Estimated number of clusters: %d (eps=.3; min=6)' % n_clusters_)
plt.savefig('Original DBSCAN plot.jpg')
plt.show()

# #############################################################################
# Original plot, point size adjusted to smaller scale

unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    if k == -1:
       col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

    Clusters = X[class_member_mask & core_samples_mask]
    plt.plot(Clusters[:, 0], Clusters[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=6)

    Outliers = X[class_member_mask & ~core_samples_mask]
    plt.plot(Outliers[:, 0], Outliers[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=2)

plt.xlim([-5,4])
plt.ylim([-5,5])
plt.title('Estimated number of clusters: %d (eps=.3; min=6)' % n_clusters_)
plt.savefig('Original DBSCAN plot (small pt size).jpg')
plt.show()

