# -*- coding: utf-8 -*-
"""
Created on Fri Oct 06 13:25:52 2017
@author: Kevin Choe w/ Brian Egner
HW1 problem3.(a),(b)
"""
#3.(a) use built in funcs to display data pts & plots of 3 diff interpolations
import matplotlib.pyplot as plt 
import numpy as np 
import scipy.interpolate as interp 
# Points provided
x_points =  np.array([1.0, 2.0, 3.0,  4.0,  5.0, 6.0, 7.0]) 
y_points =  np.array([1.0, 4.0, 10.0, 12.0, 5.0, 4.0, 0.0]) 
x = np.linspace(1,6,200) # Range from 1 to 6 
# Piecewise linear interpolation 
Pp_scipy=interp.interp1d(x_points, y_points) # built-in Piecewise int
PWvals_scipy=Pp_scipy(x)   
print('Piecewise Output:') 
print(PWvals_scipy)
plt.plot(x, PWvals_scipy,'r', label='Piecewise int')
# Lagrange polynomial interpolation
Pl_scipy = interp.lagrange(x_points, y_points) # built-in Lagrange int
Lvals_scipy=Pl_scipy(x) 
print('Lagrange data pts:') 
print(Lvals_scipy) 
plt.plot(x, Lvals_scipy, 'k',label='Lagrange int') 
 # Spline Interpolation 
from scipy.interpolate import UnivariateSpline 
Ps_scipy = UnivariateSpline(x_points, y_points) # built-in Spline int
Svals_scipy = Ps_scipy(x) 
print('Spline Output:') 
print(Svals_scipy) 
plt.plot(x, Svals_scipy,'b', label='Spline int')
#Let's indicate our points on the plot!
plt.plot(x_points, y_points, '*',label='Points')
plt.legend(loc='lower center') 
plt.axis([1, 6, 0, 13]) 
plt.grid()
plt.xlabel('X')
plt.ylabel('Y')
#3.(b) discuss the diff btw the resulting interpolations
""" In mathematical analysis, smoothness outlines how many function 
derivatives are taken and are continuous. As seen in the plot, spline has the 
worst smoothness, meaning it lacks number of data points (point derivatives) 
compare to other methods. Between the Lagrange and Piece wise interpolations, 
while both plots are smooth enough to represent quality of data sets, the 
Lagrange plot hits all 4 given points whereas the Piecewise plot still 
represented the norm of all data points. Thus, Lagrange method best 
represented not only the quantity data points (quality: smoothness) but also 
the continuity of point derivatives."""