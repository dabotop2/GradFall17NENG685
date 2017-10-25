# -*- coding: utf-8 -*-
"""
Kevin Choe  HW#2    Due:25 Oct 2017
"""
'''#HW2 Problem 2'''
import numpy as np 
import matplotlib.pyplot as plt 

h=np.array([1.0,.5,.1,.05,.01]) #Given data for h
N_Cells=np.array([8,16,80,160,800])#Given value for N Cells
rel_err=np.array([8.44660179*10**-3,2.30286448*10**-3,9.84273963*10**-5,
                  2.48043656*10**-5,9.98488163*10**-7])

'''log-log plot'''

plt.loglog(N_Cells,rel_err,"r") #Curve_fit plot
plt.title("Compaison of order of convergence by resolution discretization (log-log plot)")
plt.xlabel("Number of mesh cells(N cells)")
plt.ylabel("rel err")
plt.axis([8,800,9.98488163*10**-7,8.44660179*10**-3])
plt.grid()

plt.figure(2)
plt.loglog(h,rel_err,"b") #Data plot
plt.title("Compaison of order of convergence by resolution discretization (log-log plot)")
plt.xlabel("Mesh spacing(h)")
plt.ylabel("rel err")
plt.axis([.01,1,9.98488163*10**-7,8.44660179*10**-3])
#plt.axis([-0.001, 0.03, -0.001, 0.04])
plt.grid()

'''What is the functional relationship between error and mesh spacing/number 
of cells?

For a given set of data(rel error in this case), the more  number of cells
(the higher resolutions) we cause, the smaller mesh spacing the plot gets 
(increasing convergence rate). Also, the mesh spacing and number of mesh cells
have one by one relationship, meaning they are related to measured dataset 
linearly but not exponentially.'''
