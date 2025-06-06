Automated Voronoi‑Honeycomb Pipeline

A lightweight, proof‑of‑concept workflow for generating, organising and exporting Voronoi‑based, disordered honeycomb lattices that are ready for 3‑D printing or finite‑element analysis.The project is split into three independent but chainable modules:

Seed‑Generation (Python) – produces spatially‑inhibited point sets and writes each run to a neatly named CSV.

Parametric Modelling (Rhino 8 + Grasshopper) – converts a CSV + three high‑level parameters (bounding box, ligament thickness, extrusion depth) into a watertight 3‑D lattice.