# Automated Voronoi‑Honeycomb Pipeline

A lightweight, proof‑of‑concept workflow for generating, organising and exporting Voronoi‑based, disordered honeycomb lattices that are ready for 3‑D printing or finite‑element analysis.The project is split into two independent but chainable modules:

 Seed‑Generation (Python) – produces spatially‑inhibited point sets and writes each run to a neatly named CSV.

 Parametric Modelling (Rhino 8 + Grasshopper) – converts a CSV + three high‑level parameters (bounding box, ligament thickness, extrusion depth) into a watertight 3‑D lattice.


## 1 - Quick install
```bash
# clone the repo
git clone https://github.com/qbn-777/CapStone_stl_Automation.git
cd CapStone_stl_Automation

# Python side (Windows 11, PowerShell / CMD)
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt   # NumPy, SciPy, rhino3dm, …
```

Grasshopper is an integrated part of Rhino 8 and does not require separate installation. To access it, open Rhino and click the green Grasshopper icon in the Standard Rhino Toolbar, or type "Grasshopper" in the command line and hit Enter. 

A trial license can be obtained and used for 90 days following this instruction https://www.rhino3d.com/download/

## In src/ interfacingPython stores Module 1 functions
Mainly consider 
src\utils\interfacingPython\funtions\PointAllocationProcess.py 
src\utils\interfacingPython\funtions\run.py

## In src/rhinoGrassHopper store Module 2 under         
src\rhinoGrassHopper\DefinitionVoronoiDisorderedHC.gh

## In assetss,under csvFile will have our logging data and each csv solution.
" (assetss/csvFile/runtime_log_SSI_314_50x50_20250520_221618.csv)" this is an example of a logging folder for a run with stamped time can be read from  20250520_221618


Contact owner if needed help with installation and setting up