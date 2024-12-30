import math

def seedMaxDis(Area, numSeed):
    # Area is the total area of the field
    # numSeed is the number of seeds to be planted
    # Returns the maximum distance between the seeds

    """ Refer to Appendix A - Designing for Disorder: The Mechanical Behaviour of 
    Bioinspired, Stochastic Honeycomb Materials  by Derek Alexandre Aranguren van Egmond (University of Toronto, 2018) """
    rMax=math.sqrt(2*Area/numSeed*math.sqrt(3)) 
    return rMax
