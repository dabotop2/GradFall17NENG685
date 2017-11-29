'''
coding: utf-8
Your First Monte Carlo Radiation Transport Code</font></h1>
This notebook supplements the lesson 9 course notes on Monte Carlo.
Let's start by setting up our environment and importing what we need.  
'''
import numpy as np
import matplotlib.pyplot as plt
'''
Problem Definition
Let's create a 1-D MC transport code. For our 1D code, we have a layer geometry
consisting of 2 materials and 4 layers:
  - 1 cm $^{235}$U
  - 3 cm H$_2$O
  - 1 cm $^{235}$U
  - 3 cm H$_2$O
We want to tally the path lengh estimate of the flux in each cell assuming a 
point source that only emits in the +x direction. Although we are transporting 
in 1D, we will assume that each we have a cross-sectional area of 1cm$^2$ 
(for volume calculations).
The starting source is a mono-energetic beam of 2.45 MeV neutrons.
For simplification purposes, scattering is assumed to be only possible into the
$\pm$x directions, but the energy of the scattered particle is not tied to the 
scattering angle (note: this is non-physical and violated the conservation of momentum).
The energy distribution of the scattered particle is a uniform distribution 
between 0 and $E_n$, where $E_n$ is the energy of the incident scattered neutron.
We will consider only two reactions - scattering and absorption. The cross-section 
is assumed to be constant. 

Let's start by writing each of the key functions, and then we can pull it all
together at the end. First, let's define some basic problem parameters:
*Note:* The code here isn't the best way of managing the data, but it is explicit
and works for this simple problem.  How could we do this better?
 Define the MACROSCOPIC cross-section [cm^-1] 
 '''
h20XSec = {"scatter": 1.1, "abs": 0.1}
uXSec =  {"scatter": 2.1, "abs": 1.5}
# Define problem boundaries locations
boundaries = [0, .1, .4, .5, .8]
volumes = np.array([.1, .3, .1, .3])
# Define the materials and total cross-section in each boundary
materials = [0, 1, 0, 1]
totXSec = [3.6, 1.2, 3.6, 1.2]
# Sample Discrete CDF
# We need to develop a method to sample a discrete CDF for sampling the cross-sections.  
#For this, we can borrow from the function created in Lesson 8.
# Define pdfs
xSecPDF = [{"scatter": 0.583, "abs": 0.417}, {"scatter": 0.917, "abs": 0.083}]

# Define a CDF
xSecCDF =  [{"scatter": (0.0, 0.583), "abs": (0.583, 1.0)}, {"scatter": (0.0, 0.917), "abs": (0.917, 1.0)}]

# Create a function to sample discrete CDFs
def sampDiscrete(cdf):
    r = np.random.rand()
#    print ('r',r)
    for k, v in dict(cdf).items():
#        print ('v0',v[0])
#        print ('v1',v[1])
        if r > v[0] and r < v[1]:
            return k
'''        
#Test your discrete function
tally = {"scatter": 0, "abs": 0}
for i in range(10000):
    tally[sampDiscrete(xSecCDF[0])] += 1
print (tally)
#Define a Particle Class 
#This class determines everything about the particle and tracks all of its 
#information throughout the problem.
'''

class particle(object):
    '''
    The class creates a particle object that represents the history of a 
    transport particle. This class is created with this simplified 1D 
    problem in mind, but it could be extended to further dimensions.
    '''
    def __init__(self, xLoc=0.0, direction=1, energy=2.45, cell=0):
        """
        Constructor to build the particle class.
        @param self: <em> object pointer </em> \n
            The object pointer. \n
        @param xLoc: \e float \n
            The x coordinate location history. \n
        @param direction: \e integer \n
            The direction of the particle - options are +/-1. \n
        @param energy: \e float \n
            The energy of the particle. \n
        @param cell: \e integer \n
            The current cell location of the particle. \n
        """
        ## @var xLoc: \e float
        # The x coordinate location history.
        self.xLoc = xLoc
        ## @var direction: \e integer
        # The direction of the particle - options are +/-1.
        self.direction = direction
        ## @var energy: \e float
        # The energy of the particle.
        self.energy = energy
        ## @var cell: \e integer
        # The current cell location of the particle.
        self.cell = cell
        ## @var tally: <em> list of floats </em>
        # The tally of the path length traversed by cell
        self.tally = np.array([0., 0., 0., 0.])

    def __repr__(self):
        """!
        Particle print function.
        @param self: <em> particle pointer </em> \n
            The particle pointer. \n
        """
        return "Particle({}, {}, {})".format(self.xLoc, self.energy,
                                            self.cell)
    def __str__(self):
        """!
        Human readable particle print function.
        @param self: <em> particle pointer </em> \n
            The particle pointer. \n
        """
        header = ["\Particle:"]
        header += ["X        E      Cell"]
        header = "\n".join(header)+"\n"
        tmp = ""
        tmp += "{0:<7}{1}{2}\n".format(self.xLoc, self.energy, self.cell)
        header = header + tmp
        return header

# ### Sample the distance to the next collision
# The idea approach would be to make some of the subsequent functions methods of the particle class, but that detracts from the readability within the notebook. There is python packages that can enable the definition of a class over multiple cells (pdc), but we don't have that at AFIT.
# From the course notes, we can sample the number of MFPs to the next collision by 
# $$ n_c = -ln(\xi).$$
# From there, we can determine the distance in the current material according to
# $$ s_c = \frac{n_c}{\Sigma_{t,i}}$$
# where $i$ denotes the material that composes the cell.
# Let's write a function to add an attribute to the particle class that saves $n_c$, and let's write a function that calculates the distance to the next collision site provided a cross-section.  
        
#! Write a function to sample the number of MFP and save it to the particle class
def calcNumMFP(particle):
    r = np.random.rand()
    particle.numMFP=-np.log(r)
    
# Calculate the distance to the next collision given a number of collisions and a total cross-section
def distToCol(numMFP, xSec):
    return numMFP/xSec

# ### Find distance to next boundary
#! Write a function to calculate the distance to the next boundary
def calcDistToBound(particle, bounds):
    if particle.direction == 1:
        return boundaries[particle.cell + 1] - particle.xLoc
    elif particle.direction == -1:
        return particle.xLoc - boundaries[particle.cell]
    else:
        print ("Error: your particle is moving awkwardly!")
# ### Sample the energy distribution   
# Sample the energy loss in a collision and update the particles energy.  Assume that a single scatter, regardless of material, can lose all of the energy, and it is equally probably to lose any amount of energy from zero to all in a single collision.
        
def updateEnergy(particle):
    particle.energy = particle.energy - np.random.rand()*(particle.energy)

# ### Sample the direction
def updateDir(particle):
    r = np.random.rand()
    if r < 0.5:
        particle.direction = particle.direction*-1 
    else:
        particle.direction = particle.direction*1

# ### Transport the Particle
#! Write a function to transport a particle from the branch point in Figure 1 from Lesson 9 notes.
def transport(particle, s_b, s_c, CDF, materials, bounds, totXSec):
    while particle.energy>100:   # Kill neutron at 100 eV
        #print ('SC_TOP',s_c)
        #print ('SB_TOP',s_b)
        if s_c<=s_b:
            particle.xLoc= particle.xLoc+s_c*particle.direction
            particle.tally[particle.cell]+=s_c
            if sampDiscrete(xSecCDF[0])=='scatter':
                updateDir(particle)
                updateEnergy(particle)
                calcNumMFP(particle) 
                s_c=distToCol(particle.numMFP, totXSec[particle.cell])
                s_b=calcDistToBound(particle, bounds)
            else: 
                return
#Part(b)
        elif s_c>s_b:
            particle.xLoc= particle.xLoc+s_b*particle.direction
            particle.tally[particle.cell]+=s_b
            particle.numMFP=particle.numMFP*(1-s_b*totXSec[particle.cell]) 
            if particle.direction>=1:
                particle.cell=particle.cell+1
            elif particle.direction<1:
                particle.cell=particle.cell-1
            else:
                print ('Particle is lost at the boundary')
            # Check if particle will leak from the slab 
            if particle.xLoc==boundaries[0] and particle.direction<0:
                return
            elif particle.xLoc==boundaries[4] and particle.direction>0:
                return
            # Update s_b and s_c 
            s_c=distToCol(particle.numMFP, totXSec[particle.cell])
            #print ('s_cBot',s_c)
            s_b=calcDistToBound(particle, bounds)
            #print ('S_b_bot',s_b)
        else: 
            print('particle has not transported')

#Part (c)
N = 2000
particle.tally=np.array([0., 0., 0., 0.])  
# This is here to reset the particle tally for a new run. 
for i in range(N):    
    # Init particle. 

    particle.direction=1      # particle direction to +side(to the right) 
    particle.energy=2450000   # given 2.45 MeV neutrons 
    particle.cell=0           # start from the 0th boundary
    particle.xLoc=0         # Particle is at 0.
    # calculate s_b and s_c 
    calcNumMFP(particle)   # Give an initial MFP
    s_c=distToCol(particle.numMFP,totXSec[0])
    s_b=calcDistToBound(particle,boundaries)
    #print ('sb1',s_b)
    #print ('sc1',s_c)
    transport(particle,s_b,s_c,xSecCDF, materials,boundaries,totXSec)
print ('The number of source particles is',N)
for i in range(0,len(materials)):
    print "flux for cell:", format(particle.tally[i]/N), "n/cm^2/src particle"
    print "relative errors in cell:", format(((particle.tally[i])**(1/2))/(particle.tally[i]))