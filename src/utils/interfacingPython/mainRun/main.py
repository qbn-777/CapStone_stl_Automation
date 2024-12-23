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
    #Run for simple csbinproc allogrithm, this will work for ratio less than 0.3, but takes long time for the rest    xRecMin = 0
    # Parameters
    xRecMin=0
    xRecMax = 50
    yRecMin = 0
    yRecMax = 50
    ratio=[0.1,0.2,0.3] # ratio of the regularity
    n=314 # number of points to generate


    # (xp1,yp1),(xp2,yp2),(xp3,yp3),(xp4,yp4)
    # (0,0),(50,0),(50,50),(0,50) last (0,0) is to ensure the polygon is closed
    xp=[xRecMin, xRecMax, xRecMax, xRecMin, xRecMin]
    yp=[yRecMin,yRecMin, yRecMax, yRecMax, yRecMin]
    
    # Create the PoissonProcess object
    allocator = pp(xp, yp)
    
    
    A= Path.area(Path(np.column_stack((xp, yp)))) # Basal area
    print ("Area of the polygon is", A)
if __name__ == "__main__":

    main()