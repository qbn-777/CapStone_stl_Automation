import numpy as np
from matplotlib.path import Path
import math
from scipy.spatial.distance import pdist
import os
from datetime import datetime
from multiprocessing import Process
import time
import csv

class PointAllocationProcess:
    def __init__(self, xp, yp,method='NotDefinedAllogrithm'):
        """
        Initialize a point-allocation process for generating Poisson-like samples
        inside a 2D polygon (here, a rectangle or any area defined by xp, yp).

        Parameters:
            xp (list or np.ndarray): x-coordinates of the polygon vertices (in order).
            yp (list or np.ndarray): y-coordinates of the polygon vertices (matching xp).
            method (str): A short label indicating which sampling algorithm will be used
                          (e.g. 'SSI', 'Bridson', 'BestCandidate', etc.). Defaults to
                          'NotDefinedAlgorithm'.
        
        After initialization, these instance attributes are set:
            self.xp, self.yp: The polygon’s vertices.
            self.minx, self.maxx: Minimum and maximum x-value among the vertices.
            self.miny, self.maxy: Minimum and maximum y-value among the vertices.
            self.method: A string tag you can later use to identify which sampler generated each output file."""
      
        self.xp = xp
        self.yp = yp
        self.minx, self.maxx = min(xp), max(xp) # Min and max x-coordinates of the polygon 
        self.miny, self.maxy = min(yp), max(yp) # Min and max y-coordinates of the polygon
        self.method=method # Method to be used for point generation
        
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

            # Check if the point is inside the polygon
            # If it is, store the point in the array
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

        # Use the contains_point method to check if the point is inside the polygon
        return polygon.contains_point((x, y))
    
    def getAreaQUAD(self):
        """
        !!!! NOTED: This method is specific to rectangles and squares. !!!

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
    

    def exampleRun_SSI(self, numP, ratio, timeout):

        """
        Runs one seed generation attempt using the SSI method and saves the result
        to a structured folder system for a rectangle or square.
        This method is designed to be called multiple times with different parameters

        Parameters:
            numP (int): Number of seeds to generate.
            ratio (float): Ratio used to determine inhibition distance relative to theoretical spacing.
           

        Notes:
            - The output directory structure includes the size of the bounding rectangle, 
              derived from the polygon’s axis-aligned bounding box.
            - For irregular or non-rectangular domains, future implementations may require a more accurate
              or descriptive naming system, such as polygon type, input label, or manually defined ID.
        """
        # Define the method to be used, this only define the name, not the algorithm
        self.method = "SSI"

        # Calculate area and distances
        Area = self.getAreaQUAD()
        seedMaxDis = self.SeedMaxDis(Area, numP)
        inhibitionDis = ratio * seedMaxDis

        X = np.zeros((numP, 2))  # Container for seed points

        # Generate the first point
        point = self.generate_points(1)[0]
        X[0, :] = point
        i = 1

        # Start timing only after the first valid seed
        start_time = time.time()

        while i < numP:
            if time.time() - start_time > timeout:
                print(f" Timeout: ratio {ratio:.2f} | sample {i+1}")
                return "Timeout",time.time() - start_time
            
            point = self.generate_points(1)[0]
            sx, sy = point[0], point[1]

            xt = np.vstack(([sx, sy], X[:i, :]))
            dist = pdist(xt)
            ind = np.where(dist[:i] <= inhibitionDis)[0]

            if len(ind) == 0:
                X[i, :] = [sx, sy]
                i += 1
        
        #Take the time after the last point is generated
        total_time = time.time() - start_time

        # Determine size of the bounding quadrilateral
        width = self.maxx - self.minx
        height = self.maxy - self.miny

        base_dir = os.path.join("assetss", "csvFile", f"{width}x{height}", f"numP_{numP}", f"ratio_{ratio:.2f}")
        os.makedirs(base_dir, exist_ok=True)

        # Count how many files already exist for this method
        existing_files = [f for f in os.listdir(base_dir) if f.startswith(self.method) and f.endswith('.csv')]
        next_index = len(existing_files)

        # Save using method name + simple index (e.g. SSI_0.csv, SSI_1.csv, etc.)
        filename = f"{self.method}_{next_index}.csv"
        csv_path = os.path.join(base_dir, filename)

        np.savetxt(csv_path, X, delimiter=",")
        print(f"File saved as {csv_path}")

        return "Completed", total_time  
    
    def exampleRun_SSI_withRejects(self, numP, ratio, timeout):
        """
        1) Runs SSI until either numP seeds are placed or timeout is reached for a rectangle or square boundary
        2) Saves the resulting seeds to CSV in a structured folder system.
        3) Returns (status, runtime, attempts, rejects for analysis.
  
        Returns: N   
            status (str): "Completed" or "Timeout"
            run_time (float): seconds from first placement to finish/timeout
            attempts (int): how many random draws were made
            rejects  (int): how many of those draws were discarded
        """
        # precompute distances
        A                 = self.getAreaQUAD() # Specific to rectangle or square
        seedMax           = self.SeedMaxDis(A, numP) # Obtain maximum distance between seeds
        inhibitationDis   = ratio * seedMax # Calculate inhibition distance based on ratio and maximum distance

        # Main container to store points
        # Initialize with zeros, will be filled with points
        X       = np.zeros((numP, 2))
        X[0]    = self.generate_points(1)[0] # Place the first point can be anywhere in the polygon

        #Trackers to be reported
        placed  = 1      # Number of points successfully placed
        attempts= 1      # Number of attempts made to place points
        rejects = 0      # Number of points rejected due to inhibition distance

        t0 = time.time()
        status = "Completed" # Default status, will change to "Timeout" if we exceed the time limit

        #This is where the main loop for SSI starts
        # Keep trying to place points until we reach numP or timeout
        while placed < numP:
            # Ensure we do not exceed the timeout
            if time.time() - t0 >= timeout:
                status = "Timeout"
                break # end of while loop

            # Generate a new point
            # This is the point that will be checked against existing points
            # and placed if it does not violate the inhibition distance
            pt = self.generate_points(1)[0]
            attempts += 1

            # check against existing
            d = pdist(np.vstack([pt, X[:placed]]))[:placed]
            if (d <= inhibitationDis).any():
                rejects += 1
                continue  # jumps back to `while` top

            X[placed] = pt
            placed   += 1

        run_time = time.time() - t0

        # save CSV of the final configuration
        w,h = self.maxx - self.minx, self.maxy - self.miny
        base = os.path.join("assetss","csvFile",
                            f"{w}x{h}", f"numP_{numP}",
                            f"ratio_{ratio:.3f}")
        os.makedirs(base, exist_ok=True) #if not exists,create the directory


        fn = f"{self.method}_{len(os.listdir(base))}.csv"
        np.savetxt(os.path.join(base,fn), X, delimiter=",")
        print("Saved", fn , "to", base)

        return status, run_time, attempts, rejects

