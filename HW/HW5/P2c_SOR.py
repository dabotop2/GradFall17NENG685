import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags

#Part1
def calcIter(spectral_radius, error):
    return np.log10(error)/np.log10(spectral_radius)

print "Graphite = {}".format(calcIter(0.9948, .01))
print "Heavy Water = {}".format(calcIter(0.9998, .01))
print "Iron = {}".format(calcIter(0.6120, .01))

#Part2
from numpy.linalg import norm

def rel_converg(x_k, x_k1):
    return norm(x_k-x_k1, 2)/norm(x_k1, 2)
    
#create n matrices

n = 5 #control value to change size of the matrices,A,b,x_k, etc

k = np.array([-1*np.ones(n-1),3*np.ones(n),-1*np.ones(n-1)]) #tri matrix A, step1
offset = [-1,0,1] #tri matrix A, step2
A = diags(k,offset).toarray() #tri matrix A, step3

b = 100*np.ones(n)
x_k = np.zeros(n)

x_kP1 = np.ones(n) #Added this array for x^(k+1)


#SOR
#!  Create a SOR interative solver function
def SOR(A, x_k, x_kP1, b, i):
    
    # Initialize Values
    sum1 = 0
    sum2 = 0
    Omega= 1.15  #A splash of control added for SOR
    
    # Sum over j
    for j in range (0, i):
        sum1 += A[i, j] * x_kP1[j] #Keep x_kP1 for SOR
    for j in range (i+1, len(x_k)):
        sum2 += A[i, j] * x_k[j]
    x_k1 = ((1 - Omega)*x_k[i])+(Omega / A[i, i]) *(b[i] - sum1 - sum2)
    return x_k1

#! Write main GS solver program; report the num of iterations, the solution, and plot the convergence
import copy as cp

convTol = 10**(-6)
conv = [1]
x_k1 = cp.copy(x_k)
numIter = 0
    
while conv[-1] > convTol:
    numIter += 1
    x_k = cp.copy(x_k1)
    for i in range(0, len(x_k)):
        x_k1[i] = SOR(A, x_k, x_k1, b, i)
    conv.append(rel_converg(x_k, x_k1))
    
print "The SOR Method took {} iterations and the solution was: \n{}".format(numIter, x_k1)
Error = x_k1 - x_k
print "Error:\n", Error

plt.plot(range(len(conv)), conv,'k',label='SOR')
plt.xlabel('Generation',fontsize=12)
plt.ylabel('Relative error [%]',fontsize=12)
plt.title('SOR Convergence Plot',fontsize=14)
plt.axis([1, len(conv), convTol, 1])
plt.legend();