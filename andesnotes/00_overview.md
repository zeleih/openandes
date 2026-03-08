#ANDES Study Notes - Overview

Source: `https://docs.andes.app/en/latest/` (Homepage)

## Project positioning
- ANDES is an open source Python power system modeling and numerical analysis library.
- Core competencies:
  - Power Flow
  - Time-domain Simulation/Transient Stability (Time-domain Simulation)
  - Small perturbation stability (Eigenvalue Analysis)
  - Symbolic-numeric hybrid framework (for rapid model prototyping)
  - Support second generation new energy model

## Document structure (main navigation)
- Tutorials
- Modeling Guide
- Reference
- Verification
- ABOUT ANDES

## Key entrance
- PDF Manual: `https://docs.andes.app/_/downloads/en/stable/pdf/`
- GitHub: `https://github.com/CURENT/andes`
- PyPI: `https://pypi.org/project/andes/`

## Quick installation
- conda: `conda install -c conda-forge andes`

## Quick example
- `andes.load(andes.get_case('ieee14/ieee14_fault.xlsx'))`
- `ss.PFlow.run()`
- `ss.TDS.run()`
- `ss.TDS.plt.plot(ss.GENROU.omega)`

## Learning Paths (the path given on the home page)
- New User:
  - Installation
  - First Simulation
  - Power Flow Analysis
- Power System Analyst:
  - Data and File Formats
  - Eigenvalue Analysis
  - Parameter Sweeps and Batch Processing
- Model Developer:
  - Inspecting Model Equations
  - Hybrid Symbolic-Numeric Framework
  - Creating Models

## My understanding
- ANDES documents are typical Sphinx technical documents with clear paths and are suitable for hierarchical learning based on "user roles".
- The most important for my current task (perusing the manual) is: Tutorials + Modeling Guide + Reference.
