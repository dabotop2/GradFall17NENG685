# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 14:20:27 2017
@author: kchoe
"""
import math as m
import numpy as np 
import matplotlib.pyplot as plt
from math import sqrt
#Function
def integ(x):
    return x/m.sqrt((x**2)-1)
#Main Function 
def CompSimp38(f=None,a=None,b=None,n=None):
    integral = 0
    h=(b-a)/n
    for i in range(int(n/3)):
        integral=integral+((3*h)/8)*(f(i+a)+3*f(i+a+h)+3*f(i+a+2*h)+f(i+a+3*h))
        return integral       
#Now let's calculate the rate of convergence:       
#First, set up for CompSimp3/8
N=np.arange(3,180,3) #N divisible by 3!
a=2
b=4
Mesh_Pt=(b-a)/N
C_Simp=np.zeros(len(N)) #initialize before for loop
for i in range(0,len(N)):
    C_Simp[i]=CompSimp38(integ,a,b,N[i])
#Set up for analytical solution
a_val=(sqrt(15)-sqrt(3))*np.ones(len(N))
Numerator=abs(C_Simp-a_val)
Denominator1=abs(C_Simp-a_val)**1 #order of convergence=1
Denominator2=abs(C_Simp-a_val)**2 #order of convergence=2
Denominator3=abs(C_Simp-a_val)**3 #order of convergence=3

mu1=Numerator/Denominator1 #when q=1
mu2=Numerator/Denominator2 #when q=2
mu3=Numerator/Denominator3 #when q=3

print ("The rate of convergence(mu) when the order of convergence(q)=1:",mu1)
print ("The rate of convergence(mu) when the order of convergence(q)=2:",mu2)
print ("The rate of convergence(mu) when the order of convergence(q)=3:",mu3)

#plot mu vs h
#plt.axis(0,100,0,100)
plt.loglog(Mesh_Pt,mu1,'g*',label='mu @ q=1')
plt.loglog(Mesh_Pt,mu2,'k*',label='mu @ q=2')
plt.loglog(Mesh_Pt,mu3,'r*',label='mu @ q=3')
plt.xlabel('Grid Spacing [h]')
plt.ylabel('The rate of convergence')
plt.legend(loc='best')
plt.title("Convergence Rate")
plt.grid()