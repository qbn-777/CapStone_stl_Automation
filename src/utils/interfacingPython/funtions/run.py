import PointAllocationProcess as Process
import os, csv
from datetime import datetime

def run_example_50x50():
    typeNumb = 100 # Number of samples to run for each ratio
    timeout  = 60*3           # 3 minutes timeout
    ratios   = [0.1 + .01*i for i in range(50)]    # Starting from 0.10 to 0.59
    numP     = 314 # Number of points to allocate
    xp, yp   = [0,50,50,0,0],[0,0,50,50,0] # Polygon coordinates for a square

    # Create a PointAllocationProcess instance
    # The example run will output 1 cvs file, and return a tuple with the following values:
    # (status, runtime, attempts, rejects)
    runner = Process.PointAllocationProcess(xp, yp) 
    runner.method = "SSI" 

    # Calculate the width and height of the rectangle
    w = runner.maxx - runner.minx
    h = runner.maxy - runner.miny

    # Log header
    log = [("Method","numP","Width","Height",
            "Ratio","Sample","Time_s","Status",
            "Attempts","Rejects")]
    
    # Flag to indicate if a timeout occurred
    timeouted = False #Flag
    try:
        for r in ratios:
            for i in range(typeNumb):
                #The example run will output 1 cvs file, and return a tuple with the following values:
                #Blocking call
                status, rt, at, rj = runner.exampleRun_SSI_withRejects(numP, r, timeout)

                # Append the results to the log in a structured way
                # The log will contain the method, number of points, width, height,
                # ratio, sample number, runtime, status, attempts, and rejects
                log.append((runner.method, numP, w, h,
                            f"{r:.3f}", i,
                            f"{rt:.3f}", status,
                            at, rj))
                
                # Print a message if the status is "Timeout"
                if status == "Timeout":
                    print(f"⏱ Timeout @ ratio={r:.3f}, sample={i}")
                    timeouted= True
                    break # break the inner loop
                
                # If timeouted is True, break the outer loop
                # This is to prevent further iterations after a timeout
                if timeouted:
                    break # break the outer loop
    
    except KeyboardInterrupt:
        print("\n🛑 Interrupted — partial log will be saved.")

    # always write one runtime_log CSV
    base = os.path.join("assetss","csvFile")
    os.makedirs(base, exist_ok=True) # Ensure the directory exists
    ts = datetime.now().strftime("%Y%m%d_%H%M%S") # Timestamp for the filename
    fn = f"runtime_log_{runner.method}_{numP}_{w}x{h}_{ts}.csv" # Filename with method, numP, width, height, and timestamp
    path = os.path.join(base, fn)
    with open(path,"w",newline="") as f:
        csv.writer(f).writerows(log) # Write the log to the CSV file

    print(f"✅ Runtime log saved to {path}")

def run_example_50x50_for_long_iteration():
    """This run is for long iterations, lower iteration per ratio, and longer timeout. """
    typeNumb = 5 # Number of samples to run for each ratio
    timeout  = 60*60         # 1 hour timeout
    ratios   = [0.50 + .01*i for i in range(50)] # Starting from 0.50 to 0.99
    numP     = 314
    xp, yp   = [0,50,50,0,0],[0,0,50,50,0]

    runner = Process.PointAllocationProcess(xp, yp)
    runner.method = "SSI" 
    w = runner.maxx - runner.minx
    h = runner.maxy - runner.miny

    # Log header
    log = [("Method","numP","Width","Height",
            "Ratio","Sample","Time_s","Status",
            "Attempts","Rejects")]
    timeouted = False #Flag
    try:
        for r in ratios:
            for i in range(typeNumb):
                #The example run will output 1 cvs file, and return a tuple with the following values:
                #Blocking call
                status, rt, at, rj = runner.exampleRun_SSI_withRejects(numP, r, timeout)

                log.append((runner.method, numP, w, h,
                            f"{r:.3f}", i,
                            f"{rt:.3f}", status,
                            at, rj))
                
                if status == "Timeout":
                    print(f"⏱ Timeout @ ratio={r:.3f}, sample={i}")
                    timeouted= True
                    break # break the inner loop

                if timeouted:
                    break # break the outer loop
    
    except KeyboardInterrupt:
        print("\n🛑 Interrupted — partial log will be saved.")

    # always write one runtime_log CSV
    base = os.path.join("assetss","csvFile")
    os.makedirs(base, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fn = f"runtime_log_{runner.method}_{numP}_{w}x{h}_{ts}.csv"
    path = os.path.join(base, fn)
    with open(path,"w",newline="") as f:
        csv.writer(f).writerows(log)

    print(f"✅ Runtime log saved to {path}")

if __name__=="__main__":
    run_example_50x50_for_long_iteration()

