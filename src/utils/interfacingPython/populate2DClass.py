import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform
from matplotlib.path import Path
import seedMaxDis as smd


class populate2DClass:
    def __init__(self,xp,yp,n):
        self.xp_=xp
        self.yp_=yp
        self.n_=n
        self.x_=[]#list to store GENERATED x coordinates
        self.y_=[] #list to store GENERATED y coordinates
        
        pass

    def populator(self):
        """
        Generate homogeneous 2-D Poisson process within a polygon(eg. triangle, quadrilateral, pentagon, hexagon, octagon).
        
        Parameters:
            xp, yp: Lists for Coordinates of the polygon vertices.
            n: Number of points to generate.

        Returns:
            x, y: Coordinates of the points generated inside the polygon.
        """
        #Clear to prevent lists from being reused in next iteration
        self.x_.clear() #clear the list of x coordinates
        self.y_.clear() #clear the list of y coordinates

        minx, maxx = min(self.xp_), max(self.xp_) #minimum and maximum x coordinates of the list
        miny, maxy = min(self.yp_), max(self.yp_) #minimum and maximum y coordinates of the list
        
        while len(self.x) < self.n_:
            xt = np.random.uniform(minx, maxx)
            yt = np.random.uniform(miny, maxy)
            if self.in_polygon(xt, yt, self.xp_, self.yp_):
                self.x_.append(xt)
                self.y_.append(yt)
        

    def in_polygon(self):
        """
        Check if a point (x, y) is inside a polygon defined by vertices (xp, yp).
        Param used x,y, xp, yp
        """
    
        polygon = Path(np.column_stack((self.xp_, self.yp_)))
        return polygon.contains_point((x, y))

    def main(self):
        #Example of how to contruct a function of the class

        # Parameters
        ratio = 0.1
        n = 314
        A = 50 * 50  # Basal area
        r=smd.seedMaxDis(A, n)
        
        s = ratio * r

        # Generate the vertices for the regions
        # 
        rx = [0, 50, 50, 0, 0]
        ry = [0, 0, 50, 50, 0]

        # Generate the first event
        X = np.zeros((n, 2))
        X[0, :] = np.column_stack(self.populator(rx, ry, 1))[0]
        i = 1

        # Generate other events
        while i < n:
            sx, sy = self.csbinproc(rx, ry, 1)
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
    mainRun=populate2DClass()

    for i in range(5):
        mainRun.main()
        print("Iteration", i + 1)