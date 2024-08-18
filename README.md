This is a Python package to analyze common results and make plots out of Molecular Dynamics simulation from LAMMPS.

It includes analysis and plotting of:
  1. Mean Squared Displacement (MSD) from MSD file explicitly generated from LAMMPS;
  2. Radius of Gyration (Rg) from Rg file explicitly generated from LAMMPS;
  3. Radial Distribution Function (RDF) from .rdf file explicitly generated from LAMMPS;
  4. Stress Autocorrelation Function (SAF) and viscosity from Sauto.dat file explicitly generated from LAMMPS;
  5. End-to-end distance from trajectory file of the simulation.

Each analysis and plotting is encapsulated into function form in separate .py files.
Some of the .py files include a function named analyze_multiple_xxx(). This allows plotting results from multiple simulations into 1 single plot. In those functions please change the file path(s) in places indicated by "# to be changed".
More instructions on pre-conditions can be found in the file "MD data processing.py", or contact author at keyuwang_corin@hotmail.com.
