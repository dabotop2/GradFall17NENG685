# -*- coding: utf-8 -*-
"""
Kevin Choe  HW#1    Due:13 Oct 2017
""" 
'''1(d): changed x_pts array from (c)'''
import numpy as np
import math as m

# k is the index of the lagrange polynomial
# pts are the locations where we have fixed values
# x is the point at which we're evaluating the polynomial
def L(k,pts,x):
    prod=1.0 #initial product
    for i in range(len(pts)):
        if (i != k):
            prod=prod*(x-pts[i])/(pts[k]-pts[i])
    return prod
#now, lets define a function and set pts array
def f(x):
    return np.sin((m.pi*x)/2.0)+((x**2)/4)
x_pts=np.array([0.0,1.0,2.5,4.0])
#ploting func using 100 equally spaced pts for x btw -0.5 and 4.5
x=np.linspace(-0.5,4.5,100)
L0=L(0,x_pts,x)
L1=L(1,x_pts,x)
L2=L(2,x_pts,x)
L3=L(3,x_pts,x)
#let's plot the L0,L1,L2,L3!
import matplotlib.pyplot as plt
plt.plot(x, L0, 'b')
plt.plot(x, L1, 'g')
plt.plot(x, L2, 'k')
plt.plot(x, L3, 'r')
plt.axis([-0.5, 4.5, -5, 5])
plt.xlabel('X')
plt.ylabel('Y')
plt.legend(("L0", "L1", "L2","L3"), loc="lower center")
plt.title("Lagrange Polynomials for x0-x4")
#now combine the polynomials
P3=f(x_pts[0])*L0+f(x_pts[1])*L1+f(x_pts[2])*L2+f(x_pts[3])*L3
# This is just the function evaluation
F=f(x)
f_vals = f(x_pts)
#let's plot the P3,F,Pts!
plt.show()
plt.axis([-0.5, 4.5, -5, 5])
plt.xlabel('X')
plt.ylabel('Y')
plt.grid()
plt.plot(x, P3, 'b')
plt.plot(x, F, 'g')
plt.plot(x_pts, f_vals, '*')
plt.title("Function vs Interpolation")
plt.legend(("Interpolation", "Function", "points"), loc="lower right")

"""#1(d)Discuss the differences in how well the function is interpolated using
the different point sets:
    
As the point interval (between the 2nd and 3rd x-points) becomes smaller 
(narrower from plot (d) to plot (c)), the interpolation plot represents more 
similarity in shapes to the actual function plot. More data points cause 
narrower interval which then provide better smoothness (quality) and accuracy 
to an interpolation plot!"""