#Function to calculate the expected number of elements 
# in a pairwise operation in a set of n elements

def pairWiseElementCal(n):
    ele=n*(n-1)/2
    return ele

if __name__ == "__main__":
    n=314
    print("Number of pair wise elements", pairWiseElementCal(n))