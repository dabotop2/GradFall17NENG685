import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags

# Thomas algorithm, does Gaussian elimination for a tridiagonal matrix.
# Hand it the matrix and a right hand side, it will return a solution vector.
# NOTE: You want to modify the algorithm so that the upper and lower diagonals
#       aren't treated as being negatives.
#________________________________________________________________________
def thomas(A, b):
    #solving: Ax=b
    n = np.size(b)
    u = np.zeros(n)
    v = np.zeros(n)
    x = np.zeros(n)
    # step 1
    u[0] = A[0,0]
    v[0] = b[0]
    #step 2
    for i in range(1,n): #start from 2 and end at n(reality start from 0 goes to n-1)
            u[i] = A[i,i] - A[i,i-1] * A[i-1,i] / u[i-1]
            v[i] = b[i] - A[i,i-1]*v[i-1] / u[i-1] #changed sign of the second term to positive to negative
    #step 3
    x[n-1] = v[n-1] / u[n-1]
    #step 4
    for i in range (n-2, 0 ,-1):
        x[i] = (v[i] - A[i,i+1] * x[i+1]) / u[i] #changed sign of the second term to positive to negative
    return x
#________________________________________________________________________    
#define parameters
a = 4 #in cm
D = 1 #in cm
Sigma_a = 0.2 #in 1/cm
h = 0.1 #in cm
S = 8 #in n/(cm**3*s)
#________________________________________________________________________
#Set spatial groups
x = np.linspace(-a,a, np.int((2*a)/h+1))  #in cm

#________________________________________________________________________
#Set Matrices A
def Matrix_A_b (a,D,Sigma_a,S,h):
#------------------------------------------------------------------------    
    n = np.int(2*a/h+1)
#------------------------------------------------------------------------
#Matrix A (Tri-Diagonal)
#Tri diagonal matrix elements at boundary
    U_Dia = -((2*D)/(h**2)) #Upper Diagonal
    Dia = -((2*D)/(h**2)) + Sigma_a #Diagonal
#lower Diagonal @ upper boundary do not exist.

#Tridaigonal elements
    l_dia = -D/(h**2)#lower diagonal
    dia = ((2*D)/(h**2)) + Sigma_a #diagonal
    u_dia = -D/(h**2)#upper diagonal

    k = np.array([l_dia*np.ones(n-1),dia*np.ones(n),u_dia*np.ones(n-1)]) #tri matrix A, step1

    offset = [-1,0,1] #tri matrix A, step2
    A = diags(k,offset).toarray() #tri matrix A, step3
#    add_A = np.zeros((1,n))
#    add2_A = np.zeros((n+1,1))
    #print (np.size(add_A))
#    A = np.concatenate((A, add_A)) 
#    A = np.hstack((A, add2_A))
#------------------------------------------------------------------------
#Matrix b
    b = S*np.ones(n)
#------------------------------------------------------------------------
# BOUNDARY CONDITIONS:
    A[0,0] = Dia #change the boundary value in the matrix A
    A[0,1] = 0#U_Dia #chan    A[n,n] = 0ge the boundary value in the matrix A
    A[n-1,n-1] = 1 #lower boundary (diagonal) of A matrix
    A[n-1,n-2] = 0 #lower boundary (low diagonal) of A matrix
    b[0] = 0 #first index of b array = 0
    b[n-1] = 0 #last index of b array = 0
    return A, b

#________________________________________________________________________
#Numerical Solution:
#numerical solution matrix
A,b = Matrix_A_b(a,D,Sigma_a,S,h)    
flux = thomas(A,b)

#plot numerical solution
plt.plot (x, flux,'k',label='Numerical')
plt.xlabel('x',fontsize=12)
plt.ylabel('Phi(x)',fontsize=12)
plt.title('Thomas Plot',fontsize=14)
plt.legend();
#________________________________________________________________________
#Analytical Solution:
# Equaiton from Problem 4
L = np.sqrt(D/Sigma_a)
P4_flux = S/Sigma_a*(1-(np.exp(-x/L)+np.exp(x/L))/(np.exp(-a/L)+np.exp(a/L)))
#X will be spatiel coordinates defined above
#Y will be flux

#plot analytical solution
plt.plot (x, P4_flux,'*',label='Analytical')
plt.xlabel('x',fontsize=12)
plt.ylabel('Phi(x)',fontsize=12)
plt.title('Thomas Plot',fontsize=14)
plt.legend();
#________________________________________________________________________
#Compare answers (Numerical vs Analytical)
rel_error = np.abs(flux[1:len(flux)-1]-P4_flux[1:len(flux)-1])/P4_flux[1:len(flux)-1]
absol_error = np.abs(flux-P4_flux)
print("The Maxium Absolute Error is:", (np.max(absol_error)))
print("The Maxium Relative Error is:", (np.max(rel_error)))
#________________________________________________________________________
#Problem 6
#------------------------------------------------------------------------
#h = 1cm
h1 = 1
x_h1 = np.linspace(-a,a,np.int(2*a/h1)+1)
P4_flux_h1 = S/Sigma_a*(1.0-(np.exp(-x_h1/L)+np.exp(x_h1/L))/(np.exp(-a/L)+np.exp(a/L)))
A1,b1 = Matrix_A_b(a,D,Sigma_a,S,h1)  
flux_h1 = thomas(A1,b1)
rel_error1 = np.abs(flux_h1[1:len(flux_h1)-1]-P4_flux_h1[1:len(flux_h1)-1])/P4_flux_h1[1:len(flux_h1)-1]
print ("The Maxium Relative Error (while h=1cm) is:", (np.max(rel_error1)))
#------------------------------------------------------------------------
#h = 0.5cm
h2 = 0.5
x_h2 = np.linspace(-a,a,np.int(2*a/h2)+1)
P4_flux_h2 = S/Sigma_a*(1.0-(np.exp(-x_h2/L)+np.exp(x_h2/L))/(np.exp(-a/L)+np.exp(a/L)))
A2,b2 = Matrix_A_b(a,D,Sigma_a,S,h2)  
flux_h2 = thomas(A2,b2)
rel_error2 = np.abs(flux_h2[1:len(flux_h2)-1]-P4_flux_h2[1:len(flux_h2)-1])/P4_flux_h2[1:len(flux_h2)-1]
print ("The Maxium Relative Error (while h=0.5cm) is:", (np.max(rel_error2)))
#------------------------------------------------------------------------
#h = 0.1cm
h3 = 0.1
x_h3 = np.linspace(-a,a,np.int(2*a/h3)+1)
P4_flux_h3 = S/Sigma_a*(1.0-(np.exp(-x_h3/L)+np.exp(x_h3/L))/(np.exp(-a/L)+np.exp(a/L)))
A3,b3 = Matrix_A_b(a,D,Sigma_a,S,h3)  
flux_h3 = thomas(A3,b3)
rel_error3 = np.abs(flux_h3[1:len(flux_h3)-1]-P4_flux_h3[1:len(flux_h3)-1])/P4_flux_h3[1:len(flux_h3)-1]
print ("The Maxium Relative Error (while h=0.1cm) is:", (np.max(rel_error3)))
#------------------------------------------------------------------------
#h = 0.05cm
h4 = 0.05
x_h4 = np.linspace(-a,a,np.int(2*a/h4)+1)
P4_flux_h4 = S/Sigma_a*(1.0-(np.exp(-x_h4/L)+np.exp(x_h4/L))/(np.exp(-a/L)+np.exp(a/L)))
A4,b4 = Matrix_A_b(a,D,Sigma_a,S,h4)  
flux_h4 = thomas(A4,b4)
rel_error4 = np.abs(flux_h4[1:len(flux_h4)-1]-P4_flux_h4[1:len(flux_h4)-1])/P4_flux_h4[1:len(flux_h4)-1]
print ("The Maxium Relative Error (while h=0.1cm) is:", (np.max(rel_error4)))
#------------------------------------------------------------------------
#h = 0.01cm
h5 = 0.01
x_h5 = np.linspace(-a,a,np.int(2*a/h5)+1)
P4_flux_h5 = S/Sigma_a*(1.0-(np.exp(-x_h5/L)+np.exp(x_h5/L))/(np.exp(-a/L)+np.exp(a/L)))
A5,b5 = Matrix_A_b(a,D,Sigma_a,S,h5)  
flux_h5 = thomas(A5,b5)
rel_error5 = np.abs((flux_h5[1:len(flux_h5)-1]-P4_flux_h5[1:len(flux_h5)-1])/P4_flux_h5[1:len(flux_h5)-1])
print ("The Maxium Relative Error (while h=0.01cm) is:", (np.max(rel_error5)))
#________________________________________________________________________
#Plots for problem 6
Multi_h = np.array([1, 0.5, 0.1, 0.05, 0.01])
Num_mesh_cell = 2*a/Multi_h
Max_rel_error = np.array([np.max(rel_error1), np.max(rel_error2),
                   np.max(rel_error3), np.max(rel_error4),np.max(rel_error5)])
#------------------------------------------------------------------------
plt.figure()
plt.plot (Num_mesh_cell, Max_rel_error,'k',marker='*')
plt.xlabel('Number of mesh cells',fontsize=12)
plt.ylabel('Maximum relative error',fontsize=12)
plt.title('Max rel err as a function of number of mesh cells',fontsize=14)
plt.yscale('log')
plt.xscale('log')


plt.figure()
plt.plot (Multi_h, Max_rel_error,'k',marker='*')
plt.xlabel('Mesh size',fontsize=12)
plt.ylabel('Maximum relative error',fontsize=12)
plt.title('Max rel err as a function of mesh size',fontsize=14)
plt.yscale('log')
plt.xscale('log')
