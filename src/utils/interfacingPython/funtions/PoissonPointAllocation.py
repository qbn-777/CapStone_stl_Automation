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
        Initialise the Process with the polygon vertices.
        
        Parameters:
            xp (list or np.ndarray): x-coordinates of the polygon vertices.
            yp (list or np.ndarray): y-coordinates of the polygon vertices.
        """
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

        # Define Allogrithm to be used
        self.method="SSI" #Simple Seed Inhibition

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
        # Define the method to be used
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
 
def run_example_50x50_1():
    typeNumb = 5
    timeout =  60 # seconds
    ratio_list = [0.1 + 0.01 * i for i in range(50)]
    numP = 314
    xp = [0, 50, 50, 0, 0]
    yp = [0, 0, 50, 50, 0]

    Run = PointAllocationProcess(xp, yp)
    Run.method = "SSI"  # replace if using other algorithms

    width = max(xp) - min(xp)
    height = max(yp) - min(yp)

    log = [("Method", "numP", "Width", "Height", "Ratio", "Sample Index", "Time (s)", "Status")]

    for ratio in ratio_list:
        for i in range(typeNumb):
            status, run_time = Run.exampleRun_SSI(numP, ratio,timeout=timeout)
            log.append((Run.method, numP, width, height, ratio, i, round(run_time, 4), status))

            if status == "Timeout":
                print(f"Timeout occurred for ratio {ratio:.2f}")
                break
    print(log)
    base_log_dir = os.path.join("assetss", "csvFile")
    os.makedirs(base_log_dir, exist_ok=True)

    log_filename = f"runtime_log_{Run.method}_{numP}_{width}x{height}.csv"
    log_path = os.path.join(base_log_dir, log_filename)

    with open(log_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(log)

    print(f" Runtime log saved to {log_path}")

def run_example_50x50():
    typeNumb = 100
    timeout = 5 * 60  # 5 minutes
    ratio_list = [0.1 + 0.01 * i for i in range(50)]
    numP = 314
    xp = [0, 50, 50, 0, 0]
    yp = [0, 0, 50, 50, 0]

    Run = PointAllocationProcess(xp, yp)
    Run.method = "SSI"

    width = max(xp) - min(xp)
    height = max(yp) - min(yp)

    # prepare our in-memory log
    log = [("Method", "numP", "Width", "Height",
            "Ratio", "Sample Index", "Time (s)", "Status")]

    try:
        for ratio in ratio_list:
            for i in range(typeNumb):
                status, run_time = Run.exampleRun_SSI(numP, ratio, timeout)
                log.append((
                    Run.method,
                    numP,
                    width,
                    height,
                    f"{ratio:.2f}",
                    i,
                    f"{run_time:.4f}",
                    status
                ))
                if status == "Timeout":
                    print(f"⏱  Timeout at ratio {ratio:.2f}, sample {i}")
                    break  # stop further samples at this ratio
    except KeyboardInterrupt:
        print("\n🛑  Interrupted by user — saving partial log…")
    finally:
        # no matter what happened (finish or interrupt), write out the CSV:
        base_log_dir = os.path.join("assetss", "csvFile")
        os.makedirs(base_log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = (
            f"runtime_log_{Run.method}_{numP}_"
            f"{width}x{height}_{timestamp}.csv"
        )
        log_path = os.path.join(base_log_dir, log_filename)
        with open(log_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(log)
        print(f"✅  Runtime log saved to {log_path}")
        
def run_example_70x50():
    # Define parameters
    typeNumb=5
    ratio=[0.1 + 0.01 * i for i in range(50)]  # 0.1 to 0.59
    
    #numP,shape of the polygon are picked to be these values because 
    numP=317

    # Define the vertices of the polygon (rectangle in this case)
    xp=[0, 70, 70, 0,0]
    yp=[0, 0, 50, 50,0]

    # Create the PoissonProcess object( Refer to class for functionalities)
    Run= PointAllocationProcess(xp,yp)

    for ratio_index, r in enumerate(ratio):
        for i in range(typeNumb):
            Run.exampleRun_SSi(numP, r, i)

if __name__ == "__main__":
   run_example_50x50()