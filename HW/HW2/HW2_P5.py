# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 13:38:14 2017
@author: kchoe
"""
import numpy as np
import scipy as sp

#Set up matric A
A_minusOnes=np.ones(99)-2
A_Twos=np.ones(100)*2
A=np.diag(A_minusOnes,k=-1)+np.diag(A_minusOnes,k=1)+np.diag(A_Twos,k=0)

#Set up a vertor b
b=np.arange(0,100)
np.transpose(b)

#condition number of A
print "The condition number of A is:", np.linalg.cond(A)

#Solve this prob by inverting A and multiplying b
A_Invert=np.linalg.inv(A)
Xmatix=np.dot(A_Invert,b) #x matrix: Explicit Solution

#Use scipy.linalg.solve to solve the system
S_Xmatix=sp.linalg.solve(A,b) #Scipy version x matrix: Numerical Solution

#print for solutions
print "Display x matrix (explicit solution):"
print Xmatix
print
print "Display Scipy version x matrix (Numerical Solution):"
print S_Xmatix

#plot
import matplotlib.pyplot as plt
plt.title("Explicit Solution vs Numerical Solution")
plt.plot(b, Xmatix, 'b')
plt.plot(b, S_Xmatix, 'r*')
plt.xlabel('Vector b')
plt.ylabel('Solutions')
plt.legend(("Explicit Solution", "Numerical Solution"), loc="lower center")