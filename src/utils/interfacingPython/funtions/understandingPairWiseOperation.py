import numpy as np
from scipy.spatial.distance import pdist, squareform

def main1():
    # Sample data: 2D points
    data = np.array([[1, 2], [3, 4], [5, 6] , [7, 8], [9, 10]])
    print("Data shape:\n",np.shape(data))

    # Compute pairwise distances
    distances = pdist(data)
    print("Pairwise distances \n", distances)

    # Convert to a square matrix form
    # The squareform function converts the pairwise distances to a square matrix
    # The funtion knows that the input is unique means no duplicate "distances" (ie: ab == ba) and no self distance (ie:0)
    distance_matrix = squareform(distances)
    print("Distance matrix \n",distance_matrix)


def pairWiseElementCal(n):
    #Function to calculate the expected number of elements 
    # in a pairwise operation in a set of n elements
    ele=n*(n-1)/2
    return ele

if __name__ == "__main__":
    main1()