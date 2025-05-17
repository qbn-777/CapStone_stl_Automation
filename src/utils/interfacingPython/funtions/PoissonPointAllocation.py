import numpy as np
from matplotlib.path import Path
import math
from scipy.spatial.distance import pdist
import os
from datetime import datetime
import time
class PointAllocationProcess:
    def __init__(self, xp, yp):
        """
        Initialise the Process with the polygon vertices.
        
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
            np.ndarray: Coordinates of the points generated inside the polygon.
        """
        # Initialize an array to store the coordinates
        points = np.zeros((n, 2))
        
        count = 0
        while count < n:
            # Generate random points within the bounding box of the polygon
            xt = np.random.uniform(self.minx, self.maxx)
            yt = np.random.uniform(self.miny, self.maxy)
            if self.in_polygon(xt, yt):
                points[count, 0] = xt
                points[count, 1] = yt
                count += 1

        return points

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
        Get the area of a Rectangle or Square.
        This method use dimension provided when class is initialised.

        Returns:
            float: Area of the Rectangle or Square.
        """
        Xdiff=np.max(self.xp)-np.min(self.xp)  
        Ydiff=np.max(self.yp)-np.min(self.yp)
        return Xdiff*Ydiff 
        
    def SeedMaxDis(self,Area,numP):
        """
        Get the maximum distance between the seeds.
        
        Parameters:
            numP (int): Number of seeds.
            Area (float): Area of the polygon.
        Returns:
            float: Maximum distance between the seeds.
        """
        return math.sqrt(2*Area/numP*math.sqrt(3)) 
    
    def exampleRun(self,numP,ratio):
        """
        Example run of the using the class for a Rectangle
        This limitation is due to the getAreaQUAD() method
    
        Parameters:
            numP (int): Number of seeds.
            ratio (float): Ratio of the area to be covered.
        """
        # Get the area of the Square/Rectangle
        # Can replace this with a method that calculates the area of any polygon
        # Or input directly area 
        Area=self.getAreaQUAD()     

        # Get the maximum distance between the seeds
        seedMaxDis=self.SeedMaxDis(Area,numP)
        
        # Get the inhibitation distance (minimum distance between seeds)
        inhibitationDis=ratio*seedMaxDis
        
        # Generate the first event(Seed)
        X = np.zeros((numP, 2)) #Array to store the chosen points
        ## index 0 to ensure the point [XY] correctly assigned,
        ## eventhough only one point is generated that satify the size contraint
        point=self.generate_points(1)[0] 
        

        X[0,0],X[0,1] =point[0],point[1] # Store the first point in the Main array
        del point # Clear the point variable
        i = 1  # Counter for the number of events
  
        # This loop only stops when numP points are generated 
        # That satisfy the inhibitation distance Limitation
        while i < numP:
            # Generate a random point inside the rx,ry region   
            point = self.generate_points(1)[0]
            sx = point[0]
            sy = point[1]

            #Prepare input for pdist() for checking pairwise distances
            xt = np.vstack(([sx, sy], X[:i, :]))
            dist = pdist(xt)
        
            #Store indices of that are within the inhibitation distance
            #Refer to whole array up to i index, and taking the first row of the tupple
            ind = np.where(dist[:i] <= inhibitationDis)[0]
            
            # If no points are within the inhibitation distance, add the new point to the Main array 
            if len(ind) == 0:
                X[i, :] = [sx, sy]
                i += 1
              
        # Export the points to CSV files 
        # Create the directory structure
        base_dir = "assetss/csvFile/size50_50"
        numP_dir = os.path.join(base_dir, f"numP_{numP}")
        ratio_dir = os.path.join(numP_dir, f"ratio_{ratio}")

        # Create directories if they don't exist
        os.makedirs(ratio_dir, exist_ok=True)

    
        # Save the CSV file 
        # Generate a unique file name using a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = os.path.join(ratio_dir, f"points_{timestamp}.csv")

        # Save the CSV file
        np.savetxt(csv_filename, X, delimiter=",")
        print(f"File saved as {csv_filename}")

        return None
    

    def exampleRun_s1(self, numP, ratio, sample_index, experiment_id):
        """
        Run one seed generation attempt with given parameters and save to structured folder.
        
        Parameters:
            numP (int): Number of seeds.
            ratio (float): Ratio used to calculate inhibition distance.
            sample_index (int): Index of the current sample (used for CSV naming).
            experiment_id (str): Unique identifier for this experiment batch.
        """
        # Calculate area and distances
        Area = self.getAreaQUAD()
        seedMaxDis = self.SeedMaxDis(Area, numP)
        inhibitionDis = ratio * seedMaxDis

        X = np.zeros((numP, 2))  # Container for seed points

        # Generate the first point
        point = self.generate_points(1)[0]
        X[0, :] = point
        i = 1

        while i < numP:
            point = self.generate_points(1)[0]
            sx, sy = point[0], point[1]

            xt = np.vstack(([sx, sy], X[:i, :]))
            dist = pdist(xt)
            ind = np.where(dist[:i] <= inhibitionDis)[0]

            if len(ind) == 0:
                X[i, :] = [sx, sy]
                i += 1

        # Directory and filename structure
        base_dir = os.path.join("assetss", "csvFile", f"experiment_{experiment_id}")
        ratio_dir = os.path.join(base_dir, f"ratio_{ratio:.2f}")
        os.makedirs(ratio_dir, exist_ok=True)

        csv_filename = os.path.join(ratio_dir, f"{sample_index}.csv")
        np.savetxt(csv_filename, X, delimiter=",")
        print(f"File saved as {csv_filename}")

if __name__ == "__main__":
    typeNumb=5
    ratio=[0.1 + 0.01 * i for i in range(50)]  # 0.1 to 0.59
    numP=314
    xp=[0, 50, 50, 0,0]
    yp=[0, 0, 50, 50,0]
    # Create the PoissonProcess object( Refer to class for functionalities)
    Run= PointAllocationProcess(xp,yp)

    """ for r in ratio:
        for i in range(typeNumb):
         #Take the current time
         time1 = time.time()
         Run.exampleRun(numP,r)
        #Take the current time
        time2 = time.time()
        #Find time Difference
        timeDiff = time2 - time1
        #Find average time by taking time diff divided by typeNumb """
    experiment_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    for ratio_index, r in enumerate(ratio):
        for i in range(typeNumb):
            Run.exampleRun_s1(numP, r, i, experiment_id)
