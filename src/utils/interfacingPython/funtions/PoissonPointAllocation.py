import numpy as np
from matplotlib.path import Path

class PoissonProcess:
    def __init__(self, xp, yp):
        """
        Initialize the PoissonProcess with the polygon vertices.
        
        Parameters:
            xp (list or np.ndarray): x-coordinates of the polygon vertices.
            yp (list or np.ndarray): y-coordinates of the polygon vertices.
        """
        self.xp = xp
        self.yp = yp
        self.minx, self.maxx = min(xp), max(xp) # Min and max x-coordinates of the polygon 
        self.miny, self.maxy = min(yp), max(yp) # Min and max y-coordinates of the polygon

    def generate_points(self, n):
        """
        Generate homogeneous 2-D Poisson process within the polygon.
        Parameters:
            n (int): Number of points to generate.
        
        Returns:
            x, y: Coordinates of the points generated inside the polygon.
        """
        #Empty list to store the x and y coordinates
        PointList = []
        
        while len(PointList) < n:
            # Generate random points within the bounding box of the polygon
            xt = np.random.uniform(self.minx, self.maxx)
            yt = np.random.uniform(self.miny, self.maxy)
            if self.in_polygon(xt, yt):
                PointList.append([xt, yt])

        return PointList

    def in_polygon(self, x, y):
        """
        Check if a point (x, y) is inside the polygon.
        
        Parameters:
            x (float): x-coordinate of the point.
            y (float): y-coordinate of the point.
        
        Returns:
            bool: True if the point is inside the polygon, False otherwise.
        """
        polygon = Path(np.column_stack((self.xp, self.yp)))
        return polygon.contains_point((x, y))
    
    def getAreaQUAD(self):
        """
        Get the area of a Quadrilateral.
        
        Returns:
            float: Area of the Quadrilateral.
        """
        Xdiff=np.max(self.xp)-np.min(self.xp)  
        Ydiff=np.max(self.yp)-np.min(self.yp)
        return Xdiff*Ydiff # This need to be type int
        