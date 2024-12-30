import rhino3dm as rs
import csv
import os

# Path to the folder containing your CSV files
csv_folder = r"C:\Path\To\Your\CSVFolder"
output_folder = r"C:\Path\To\Export\Folder"

# Function to read points from a CSV file
def read_csv_points(file_path):
    points = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        #next(csv_reader)  # Skip header (if present)
        for row in csv_reader:
            x, y, z = map(float, row)
            points.append((x, y, z))
    return points

# Function to export STL
def export_stl(file_name, points):
    # Clear current Rhino document
    rs.Command("_SelAll")
    rs.Command("_Delete")

    # Add points to Rhino
    for pt in points:
        rs.AddPoint(pt)
    
    # Export as STL
    stl_path = os.path.join(output_folder, f"{file_name}.stl")
    rs.Command(f'-_Export "{stl_path}" _Enter _Enter')
    print(f"Exported: {stl_path}")

def main():
    # Main routine
    for csv_file in os.listdir(csv_folder):
        if csv_file.endswith(".csv"):
            csv_path = os.path.join(csv_folder, csv_file)
            points = read_csv_points(csv_path)
            file_name = os.path.splitext(csv_file)[0]
            export_stl(file_name, points)

def mainTest():
    read_csv=read_csv_points(r"C:\Users\binhn\OneDrive\Desktop\CodeProject\capstone\XTRAWIDE_50x50_n314_0.1_NEW.csv")
    #print(read_csv)

    for pt in read_csv:
        rs.Point(pt)
if __name__ == "__main__":
    mainTest()