#Import these two to ensure the path is correct
import sys
from pathlib import Path

#Import code for main functionalities
from ..funtions.PoissonPointAllocation import PoissonProcess as pp
from ..funtions.seedMaxDis import seedMaxDis as smd 
import matplotlib.pyplot as plt
from matplotlib.path import Path
import numpy as np

def main():
    # Run for simple csbinproc algorithm.
    # This will work for ratio less than 0.3,
    xRecMin = 0
    # Parameters
    xRecMin=0
    xRecMax = 50
    yRecMin = 0
    yRecMax = 50
    ratio=[0.1,0.2,0.3] # ratio of the regularity
    n=314 # number of points to generate


    # (xp1,yp1),(xp2,yp2),(xp3,yp3),(xp4,yp4)
    # (0,0),(50,0),(50,50),(0,50) last (0,0) 
    xp=[xRecMin, xRecMax, xRecMax, xRecMin]
    yp=[yRecMin,yRecMin, yRecMax, yRecMax]
    
    # Create the PoissonProcess object
    allocator = pp(xp, yp)
    
    
    A= allocator.getAreaQUAD()
    
    print ("Area of the polygon is", A)
if __name__ == "__main__":

    main()