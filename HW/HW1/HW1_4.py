# -*- coding: utf-8 -*-
"""
Kevin Choe  HW#1    Due:13 Oct 2017
"""
'''#HW1 Problem 4 (a)-(c)'''
import numpy as np 
h=np.array([0.0500000,0.0250000,0.0125000,0.0062500,0.0031250,0.0015625,
              0.000718125,0.000390625]) #Given data for h(Grid Spacing)
E=np.array([0.103612,0.0333834,0.013754094,0.004177237,0.00113962,0.0002824698,
            0.00007185644,0.00001813937])#Given value for E(Error)
'''Matrix for A_x vector [1 ln(h)],...'''
lnH=np.log(h)#ln(h) array
lnHmat=np.asmatrix(lnH).reshape((8,1))#Change array to 8by1 Transposed matrix
n,m=lnHmat.shape    #Step1. to set up matrix w/ ones
Ones=np.ones((n,1)) #Step2. to set up matrix w/ ones
A=np.hstack((Ones, lnHmat))
'''Matrix for b vector [ln(E)],...'''
lnE=np.log(E)#ln(E) array
lnEmat=np.asmatrix(lnE).reshape((8,1))#Change array to Transpose to 8by1 matrix
'''Now let's use normal equation (transpose matrix tech) to minimize the sum
of the square differences the left and right side of our equation, 
Ax=b(ln(k)+pln(h)=ln(E)).'''
AT=A.T #A^T matrix
ATA=AT*A # A^T*A
ATb=AT*lnEmat # A^T*b
'''Let's Calculate our X matix by using least spares approx '''
Xmat= np.linalg.lstsq(ATA,ATb) # Creates a Tuple Solution
Xvector=Xmat[0]
k=np.exp(np.asscalar(Xvector[0]))#calculate k, not ln(k) by using np.exp
p=np.asscalar(Xvector[1])#0,1 for vector numbers
print("Least Square Approximation")
print("p=",p,"k=",k)

'''HW1 Problem 4 (d)'''
from scipy.optimize import curve_fit
def f(x,K,P):
    return K*x**P #Error function
KPstorage, est=curve_fit(f,h,E)
K=KPstorage[0]
P=KPstorage[1]
print("Curve_fit Approximation")
print("p=",P,"k=",K)

'''HW1 Problem 4 (e)'''
import matplotlib.pyplot as plt
x=np.linspace(-0.5,0.5,5000)#define x for plot

'''lin-lin plot'''
plt.plot(h,E,"k*") #Data plot
LS_E=k*x**p #y data for Least Squares
plt.plot(x,LS_E,"b") #Least Squares plot
CF_E=K*x**P #y data for Curve_fit
plt.plot(x,CF_E,"r") #Curve_fit plot

plt.xlabel("Grid Spacing(h)")
plt.ylabel('Error(E)')
plt.title("Linear Approximation (lin-lin plot)")
plt.legend(("Given Data","Least Squares","CurveFit"),loc="upper left")
plt.axis([-0.001, 0.03, -0.001, 0.04])
plt.grid()

'''log-log plot'''
plt.figure(2)
plt.loglog(h,E,"k*") #Data plot
plt.loglog(x,LS_E,"b") #Least Squares plot
plt.loglog(x,CF_E,"r") #Curve_fit plot
plt.xlabel("Grid Spacing(h)")
plt.ylabel('Error(E)')
plt.title("Linear Approximation (log-log plot)")
plt.legend(("Given Data","Least Squares","CurveFit"),loc="lower right")
plt.axis([-0.001, 0.03, -0.001, 0.04])
plt.grid()

'''P4 (e) discuss the differences btw LS and CF Appx.
Just by looking at the lin-lin plot, it is very hard to tell the difference 
between the two approximation methods, Curve Fitting and Least Squares. 
However, if we take a look at the log-log plot we can tell that the Least 
Squares method approximates more accurate vector of unknowns (its plot is more 
precisely shaped  similar to the actual data points. This means that if we get
 more data sets and shorten the spaces between each data point squares, the 
Least Squares method would even get a better approximation of vector of
unknowns, in comparison to the Curve fitting method.'''