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
    ratio = 0.5
    n = 314
    A = 50 * 50  # Basal area
    r=smd.seedMaxDis(A, n)
    print("Seed max dis", r)
      
    s = ratio * r

    # Generate the vertices for the regions
    rx = [0, 50, 50, 0,0]
    ry = [0, 0, 50, 50,0]

    # Generate the first event
    X = np.zeros((n, 2))
    X[0, :] = np.column_stack(csbinproc(rx, ry, 1))[0]
    i = 1

    # Generate other events
    while i < n:
        sx, sy = csbinproc(rx, ry, 1)
        xt = np.vstack(([sx[0], sy[0]], X[:i, :]))
        dist = pdist(xt)
        ind = np.where(dist[:i] <= s)[0]
        if len(ind) == 0:
            X[i, :] = [sx[0], sy[0]]
            i += 1

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
    np.savetxt("XTRAWIDE_50x50_n314_0.1_NEW.csv", np.hstack((X, np.zeros((X.shape[0], 1)))), delimiter=",")
    

def main2():
    # Parameters
    ratio = 0.8
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
    max_attempts = 1000  # Limit retries to avoid infinite loops
    attempts = 0

    while i < n:
        sx, sy = csbinproc(rx, ry, 1)  # Generate a random point inside the polygon
        dist, _ = tree.query([sx[0], sy[0]])  # Query nearest point distance
        
        if dist > s:  # Check if the point satisfies the minimum distance
            X[i, :] = [sx[0], sy[0]]
            i += 1
            tree = KDTree(X[:i, :])  # Update the KDTree with the new point
            attempts = 0  # Reset attempts
        else:
            attempts += 1
            if attempts >= max_attempts:
                print(f"Relaxing constraint at point {i} after {max_attempts} failed attempts.")
                s *= 0.9  # Relax the constraint by 10%
                attempts = 0

    # Verify and plot
    plt.scatter(X[:, 0], X[:, 1], s=10, c='blue')
    plt.title("Simple Sequential Inhibition Process with KDTree")
    plt.xlabel("X (mm)")
    plt.ylabel("Y (mm)")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
        for i in range(5):
            main2()
            print("Iteration", i + 1) 
   
    