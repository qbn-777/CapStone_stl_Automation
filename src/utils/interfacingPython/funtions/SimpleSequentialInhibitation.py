import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
from matplotlib.path import Path
import seedMaxDis as smd
from scipy.spatial import KDTree

def csbinproc(xp, yp, n):
    """
    Generate homogeneous 2-D Poisson process within a polygon.
    
    Parameters:
        xp (list or np.ndarray): x-coordinates of the polygon vertices.
        yp (list or np.ndarray): y-coordinates of the polygon vertices.
        n (int): Number of points to generate.

    Returns:
        x, y: Coordinates of the points generated inside the polygon.
    """
    x = []
    y = []
    
    minx, maxx = min(xp), max(xp) # Min and max x-coordinates of the polygon 
    miny, maxy = min(yp), max(yp) # Min and max y-coordinates of the polygon
    
    # While loop only stops when n points are generated
    # Which only possible when in_polygon returns True    
    while len(x) < n:
        # Generate random points within the bounding box of the polygon
        xt = np.random.uniform(minx, maxx)
        yt = np.random.uniform(miny, maxy)
        if in_polygon(xt, yt, xp, yp) == True:
            x.append(xt)
            y.append(yt)
    
    return np.array(x), np.array(y)

def in_polygon(x, y, xp, yp):
    """
    Check if a point (x, y) is inside a polygon defined by vertices (xp, yp).
    This function is compatible for checking any abitrary 2D shape, with n number of vertices
    
    Parameters:
    x: float, x-coordinate of the point to check
    y: float, y-coordinate of the point to check
    xp: list or np.ndarray, x-coordinates of the polygon vertices
    yp: list or np.ndarray, y-coordinates of the polygon vertices

    Returns:
    bool: True if the point is inside the polygon, False otherwise
    """
   
    # Create a Path object from the vertices
    # This function stacks the xp,and yp array into an array of shape (n, 2)
    # Where n is the number of vertices (eg, 5 for polygon)
    polygon = Path(np.column_stack((xp, yp)))

    # Check if the point is inside the polygon (Boolean output)
    return polygon.contains_point((x, y))

def main():
    # Parameters
    ratio = 0.1
    n = 314
    A = 50 * 50  # Basal area
    r=smd.seedMaxDis(A, n)
    print("Seed max dis", r)
      
    s = ratio * r
    print("Inhibitation Distance/Minimum dis between seeds", s)

    # Generate the vertices for the regions
    rx = [0, 50, 50, 0,0]
    ry = [0, 0, 50, 50,0]

    # Generate the first event
    X = np.zeros((n, 2))
    X[0, :] = np.column_stack(csbinproc(rx, ry, 1))[0]
    i = 1 # Counter for the number of events

    # Generate other events
    while i < n:
        sx, sy = csbinproc(rx, ry, 1)
        xt = np.vstack(([sx[0], sy[0]], X[:i, :]))
        dist = pdist(xt)
        ind = np.where(dist[:i] <= s)[0]
        if len(ind) == 0:
            X[i, :] = [sx[0], sy[0]]
            i += 1
            print(i)

    # Verify and plot
    dist = pdist(X)
    delhat = np.min(dist)
    xx = X[:, 0]
    yy = X[:, 1] 

    # Plotting
    plt.scatter(xx, yy, s=10, c='blue')
    plt.title("Simple Sequential Inhibition Process")
    plt.xlabel("X (mm)")
    plt.ylabel("Y (mm)")
    plt.grid(True)
    plt.show()

    # Optional: Write to CSV with relative path 
    np.savetxt("test02.csv", np.hstack((X, np.zeros((X.shape[0], 1)))), delimiter=",")
    

def main2():
    # Parameters
    ratio = 0.5
    n = 314
    A = 50 * 50  # Area of the bounding polygon
    r = smd.seedMaxDis(A, n)
    print("Seed max distance:", r)
    s = ratio * r

    # Define the vertices of the bounding polygon
    rx = [0, 50, 50, 0, 0]
    ry = [0, 0, 50, 50, 0]

    # Initialize storage for points
    X = np.zeros((n, 2))
    X[0, :] = np.column_stack(csbinproc(rx, ry, 1))[0]  # First point
    tree = KDTree(X[:1, :])  # Initialize KDTree with the first point
    i = 1

    # Generate points with KDTree for distance checking
    max_attempts = 100000  # Limit retries to avoid infinite loops
    attempts = 0

    while i < n:
        sx, sy = csbinproc(rx, ry, 1)  # Generate a random point inside the polygon
        dist, _ = tree.query([sx[0], sy[0]])  # Query nearest point distance
        
        if dist > s:  # Check if the point satisfies the minimum distance
            X[i, :] = [sx[0], sy[0]]
            i += 1
            tree = KDTree(X[:i, :])  # Update the KDTree with the new point
            attempts = 0  # Reset attempts
       

    # Verify and plot
    plt.scatter(X[:, 0], X[:, 1], s=10, c='blue')
    plt.title("Simple Sequential Inhibition Process with KDTree")
    plt.xlabel("X (mm)")
    plt.ylabel("Y (mm)")
    plt.grid(True)
    plt.show()

def main3():
    # Example for plotting the points as they are generated, hence "Interactive"

    # Parameters
    ratio = 0.1
    n = 314
    A = 50 * 50  # Basal area
    r = smd.seedMaxDis(A, n)
    print("Seed max dis", r)
      
    s = ratio * r
    print("Inhibitation Distance/Minimum dis betwwen seeds", s)
    # Generate the vertices for the regions
    rx = [0, 50, 50, 0, 0]
    ry = [0, 0, 50, 50, 0]

    # Generate the first event
    X = np.zeros((n, 2))
    X[0, :] = np.column_stack(csbinproc(rx, ry, 1))[0]
    i = 1  # Counter for the number of events

    # Set up the plot
    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()    
    scatter = ax.scatter(X[:, 0], X[:, 1], s=3, c='blue') # X = All Rows of 0th column and Y = All Rows of 1st column
    ax.set_title(f"Simple Sequential Inhibition Process for Regular Regularity = {ratio}")
    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.grid(True)
    plt.xlim(0, 50)
    plt.ylim(0, 50)
    plt.draw()

    # This loop only stops when n points are generated that are satisfying the inhibitation distance Limitation
    while i < n:

        # Generate a random point inside the rx,ry region
        sx, sy = csbinproc(rx, ry, 1)

        #Prepare input for pdist() for checking pairwise distances
        xt = np.vstack(([sx[0], sy[0]], X[:i, :]))
        dist = pdist(xt)
        #print("dist shape", np.shape(dist))

        #Store indices of points that are within the inhibitation distance
        #Refer to whole array up to i index, and taking the first row of the tupple
        ind = np.where(dist[:i] <= s)[0]
        
        # If no points are within the inhibitation distance, add the new point to the Main array 
        if len(ind) == 0:
            X[i, :] = [sx[0], sy[0]]
            i += 1
            # Update the plot
            scatter.set_offsets(X)
            plt.draw()
            plt.pause(0.1)  # Pause to update the plot

    # Verify and plot final result
    xx = X[:, 0]
    yy = X[:, 1]

    # Final plot
    plt.ioff()  # Turn off interactive mode
    plt.scatter(xx, yy, s=3, c='blue') #This s is the size of the points not the inhibitation distance
    plt.title("Simple Sequential Inhibition Process")
    plt.xlabel("X (mm)")
    plt.ylabel("Y (mm)")
    plt.grid(True)
    plt.show()

    #np.savetxt("test2000PointsR_0_1.csv", np.hstack((X, np.zeros((X.shape[0], 1)))), delimiter=",")
if __name__ == "__main__":
    main3()
            
   
    