# ANDES Study Notes - Tutorials

source:
- `tutorials/index.html`
- `tutorials/01-installation.html`

## Tutorial Overview
Tutorial link coverage:
1. Installation
2. First Simulation
3. Power Flow Analysis
4. Time-Domain Simulation
5. Data and File Formats
6. Plotting Results
7. Eigenvalue Analysis
8. Parameter Sweeps and Batch Processing
9. Contingency Analysis
10. Dynamic Control and Setpoint Changes
11. Frequency Response and Load Shedding
12. Inspecting Model Equations

### Learning Path
- New User：01-06
- Power System Analyst：07-11
- Model Developer: Complete the basics first and then enter the Modeling Guide

---

## Installation details

### Quick installation
- Recommended: `conda install -c conda-forge andes`
- Also supports pip and uv.

### Novice environment suggestions
- Recommend Miniforge + conda-forge.
- Apple Silicon recommends the `arm64` package.
- Recommended separate environment:
  - `mamba create --name andes python=3.11`
  - `mamba activate andes`

### uv path
- `uv pip install andes`
- New environment example (3.12)
- Support `andes[dev]`.

### Extend dependency group
- `dev`: tests/docs
- `interop`: interoperate with other power system tools
- all extras: `pip install andes[all]`

### Development installation
- `git clone https://github.com/curent/andes`
- `pip install -e .`
- Use `git pull` for updates in dev mode. Do not mix conda/pip to cause repeated installations.

### Upgrade and Troubleshooting
- conda: `conda install -c conda-forge --yes andes`
- pip: `pip install --upgrade andes`
- uv: `uv pip install --upgrade andes`
- Typical problems: multi-copy installation, Windows DLL load failed (conda environment is recommended).

## My understanding
- The official emphasizes "environment isolation + no mixing + version traceability (setuptools-scm)".
- ANDES clearly distinguishes the paths for developers and ordinary users in the installation strategy.
