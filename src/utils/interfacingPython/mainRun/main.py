#Import these two to ensure the path is correct
import sys
from pathlib import Path

#Import code for main functionalities
from ..funtions.PoissonPointAllocation import PoissonProcess as pp
from ..funtions.seedMaxDis import seedMaxDis as smd 
import matplotlib.pyplot as plt
from matplotlib.path import Path
import numpy as np

def main(xRecMin, xRecMax, yRecMin, yRecMax, ratio, n, maxIter):
    # Run for simple poisson point generation then check for distance requirement

    # SIMPLE SEQUENTIAL INHIBITION PROCESS%% 
    #For 50x50 surface, with n=314 seeds, delta = s/r = 0.1

    xp=[xRecMin, xRecMax, xRecMax, xRecMin]
    yp=[yRecMin,yRecMin, yRecMax, yRecMax]
    
    # Create the PoissonProcess object( Refer to class for functionalities)
    allocator = pp(xp, yp)

    # Only works for a RECTANGLE or Square
    # Create a new method for other polygons 
    A= allocator.getAreaQUAD()
    print ("Area of the polygon is", A)
    print ("Area type", type(A))
    
   
    s = ratio * smd(A, n)  
    X = np.zeros((n, 2)) #An array of zeros with n rows and 2 columns (x and y coordinates)

    X=allocator.generate_points(n=1) #This function return 2 array
    i=1 #Counter for the number of events
    
    # Loop stay active until the number of points generated is equal to n
    while i < n:
        P=allocator.generate_points(n=1)

  

if __name__ == "__main__":
   # Parameters
    xRecMin=0
    xRecMax = 50
    yRecMin = 0
    yRecMax = 50
    ratio=[0.1,0.2,0.3] # ratio of the regularity to loop through
    n=314 # number of points to generate
    maxIter=100 #Number of csv files to generate for each ratio

    main(xRecMax, xRecMin, yRecMax, yRecMin, ratio, n, maxIter)