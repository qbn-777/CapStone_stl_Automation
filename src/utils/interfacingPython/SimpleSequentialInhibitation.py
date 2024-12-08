import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
from matplotlib.path import Path

def csbinproc(xp, yp, n):
    """
    Generate homogeneous 2-D Poisson process within a polygon.
    
    Parameters:
        xp, yp: Coordinates of the polygon vertices.
        n: Number of points to generate.

    Returns:
        x, y: Coordinates of the points generated inside the polygon.
    """
    x = []
    y = []
    minx, maxx = min(xp), max(xp)
    miny, maxy = min(yp), max(yp)
    
    while len(x) < n:
        xt = np.random.uniform(minx, maxx)
        yt = np.random.uniform(miny, maxy)
        if in_polygon(xt, yt, xp, yp):
            x.append(xt)
            y.append(yt)
    
    return np.array(x), np.array(y)

def in_polygon(x, y, xp, yp):
    """
    Check if a point (x, y) is inside a polygon defined by vertices (xp, yp).
    """
   
    polygon = Path(np.column_stack((xp, yp)))
    return polygon.contains_point((x, y))

def main():
    # Parameters
    ratio = 0.1
    n = 314
    A = 50 * 50  # Basal area
    r = np.sqrt((2 * A) / (np.sqrt(3) * n))
    s = ratio * r

    # Generate the vertices for the regions
    rx = [0, 50, 50, 0, 0]
    ry = [0, 0, 50, 50, 0]

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

    # Optional: Write to CSV
    np.savetxt("XTRAWIDE_50x50_n314_0.1_NEW.csv", np.hstack((X, np.zeros((X.shape[0], 1)))), delimiter=",")

if __name__ == "__main__":
    for i in range(5):
        main()
        print("Iteration", i + 1)