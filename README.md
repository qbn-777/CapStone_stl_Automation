Automated Voronoi‑Honeycomb Pipeline

A lightweight, proof‑of‑concept workflow for generating, organising and exporting Voronoi‑based, disordered honeycomb lattices that are ready for 3‑D printing or finite‑element analysis.The project is split into three independent but chainable modules:

Seed‑Generation (Python) – produces spatially‑inhibited point sets and writes each run to a neatly named CSV.

Parametric Modelling (Rhino 8 + Grasshopper) – converts a CSV + three high‑level parameters (bounding box, ligament thickness, extrusion depth) into a watertight 3‑D lattice.

Ensure to install the requirement file to run without conflict error.

In src/ interfacingPython stores Module 1 functions
In src/rhinoGrassHopper store Module 2 under DefinitionVoronoiDisorderedHC.gh

In assetss,under csvFile will have our logging data and each csv solution.

Contact owner if needed help with installation and setting up