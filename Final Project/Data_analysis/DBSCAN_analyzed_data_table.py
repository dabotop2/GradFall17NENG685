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
import pandas as pd
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
plt.show()


# #############################################################################
# Boundary vs Core analysis

Table=np.column_stack((X,core_samples_mask,labels)) #create X/Y/Core/Label table for visual anlaysis
'''
Column2 of "Table" array: 0=F; 1=T
Column3 of "Table" array: -1=Outlier 0=<in Clusters 0 to nth Cluster
Take a look at the "Table"array in the Variable explorer,
Some column2 values says "not part of core" while column 2 values indicate that they belong to one of the clusters.
In other words, they are assumed to be boundary points!
'''
# find indicies of:
Cluster_indices=np.where(core_samples_mask == 0)#Clusters data
Outlier_indices=np.where(labels < 0)#Outliers data
Boundary_pts_indices=np.nonzero((core_samples_mask == 0) & (labels >= 0))#Boundary point data

# True=1; False=0 array for Boundary points
Boundary_base = np.zeros((1948,1))
np.put(Boundary_base,Boundary_pts_indices,1)

# True=1; False=0 array for Outliers
Outlier_base = np.zeros((1948,1))
np.put(Outlier_base,Outlier_indices,1)

#create X/Y/Core/Boundary/Outlier table for visual anlaysis
Data_summary=np.column_stack((X,core_samples_mask,Boundary_base,Outlier_base,labels))

#create Dataframe for Data_summary for better output data display
Data_Summary = pd.DataFrame(Data_summary)
Data_Summary.columns=["X data", "Y data", "Core", "Border", "Noise", "Cluster#"]
Data_Summary.to_csv('Data Summary.csv', sep=',')

'''
Final Result! 
Data summary captured in the "Data_summary" table in the Variable explorer.

Suppose we want to add a set of random data into a preexisting data set 
and compare their relation. We can simply add a new data set to preexisting data
set in "DBSCAN-data.py". Then, we operate the run file "DBSCAN_analyzed_data_table"
which is already built to import data from "DBSCAN-data.py" file. This run file 
will display useful information in the Variable explorer box (locates above the 
console box) in array forms. We can track new data sets by index numbers in arrays. 
With this run file:
    
- We can define which cluster group the new data points belong to, via looking at 
  "labels" array or "Data_Summary" table.
- We can define how strongly the new points are related to preexisting points by 
  recognizing them as core, boundary, or outlier points via looking at 
  "Data_Summary" table.
- Most importantly, we can manipulate the controlling variables such as epsilon 
  (distance between points that is used to define clusters) and minimum sample 
  number (minimum number of data points required to form clusters) to conveniently 
  analyze data.
''' 