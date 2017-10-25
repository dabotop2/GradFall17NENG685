# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 15:27:34 2017
@author: kchoe
"""
from P6_NukeData import nuclearData as ND
import numpy as np
import scipy as sp
#isotopes that we are interested in:
isotopes=['Fr-221','At-217','Bi-213','Po-213','Tl-209','Pb-209','Bi-209','Tl-205']

#OdeInt set up
def I_decay(No,t,isotopes,ND):
    half_life=np.zeros(len(isotopes)) #initialize
    lamb=np.zeros(len(isotopes))     #initialize
    lam=np.zeros(len(isotopes))       #initialize
    for i in range(0,len(isotopes)):
        half_life[i]=ND[isotopes[i]][0]
        lam[i]=np.log(2)/half_life[i]
        if i==0:                               #Fr-221
            lamb[i] += -lam[i]*No[i]
        elif i==7:                            #Ti-205
            lamb[i] += +lam[i-1]*No[i-1]
        else:                              #mid-isotopes
            lamb[i] += -lam[i]*No[i]+lam[i-1]*No[i-1]
    return lamb
#create time array for x-axis        
t=np.linspace(1,86400,10E4) #1sec to 86400sec(1day)
#t=np.linspace(1,10E5,10E4) #1sec to 10^5sec (Appx.11days)


#initialize variables for odeint
Concentration=np.array([1,0,0,0,0,0,0,0])
N=sp.integrate.odeint(I_decay,Concentration,t,args=(isotopes,ND))

# Plotting
for key in ND:
    I_label = isotopes[0]
import matplotlib.pyplot as plt
plt.plot(t,N)
plt.legend([isotopes][0])
plt.legend(loc='best')
plt.xlabel('Time(s)')
plt.ylabel('Relative Abundance')
plt.title('Np Decay Chain (from Fr to Ti)')
plt.grid()