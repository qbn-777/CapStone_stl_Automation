import math

def seedMaxDis(Area, numSeed):
    # Area is the total area of the field
    # numSeed is the number of seeds to be planted
    # Returns the maximum distance between the seeds

    #Type check for Area, numSeed
    #Area must be a number larger or equal to 0
    if type(Area) is not float :
        raise TypeError("Area must be a number")
    if Area<0:
        raise ValueError("Area must be larger or equal to 0")
    
    #numSeed must be an integer larger than 0
    if type(numSeed) is not int:
        raise TypeError("numSeed must be an integer")
    if numSeed<=0:
        raise ValueError("numSeed must be larger than 0")
    
    rMax=math.sqrt(2*Area/numSeed*math.sqrt(3))
    return rMax
