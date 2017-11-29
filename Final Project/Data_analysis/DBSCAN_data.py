# -*- coding: utf-8 -*-
"""
NENG685 Final Project
DBSCAN
@author: Kevin Choe
"""
import numpy as np
import pandas as pd

#using pandas to import data from Excel 
BDSCAN_data = pd.read_excel('DBSCAN_data.xlsx', sheetname='Sheet1')

#convert dataframe to np array
Data_array=BDSCAN_data.values

#if required adjust the # of columns (2D vs 3D)
Data_array=np.delete(Data_array,0,1) #change the middle # to delete a column of your choice

#print data array for confirmation
print(Data_array)