# ANDES Study Notes - Verification & About

source:
- `verification/index.html`
- `about.html`

## Verification

### Verification target
- Compare with commercial software to verify the correctness of the model and algorithm (time domain simulation results).

### Target object
- PSS/E
- TSAT
- Published benchmark data

### Typical system
- IEEE 14-bus: highly consistent results
- NPCC: Multi-region multi-model system, comparison of commercial tools
- WECC: A large system contains new energy, and there are slight differences (it is difficult for multiple tools to be completely consistent in a large system)

### Comparison method
- Parameters consistent
- perturbation consistent
- Time steps should be as comparable as possible
- Comparison variables: rotor angle, speed, bus voltage

## About

### Project positioning
- ANDES is one of the dynamic simulation engines of CURENT Large Scale Testbed.

### Core Technology
- Symbolic-numeric hybrid framework:
  - Python + SymPy writing model
  - Automatically generate optimized numerical code
  - Code cache reuse (symbol overhead is not paid every time)

### Capability declaration (given in the document)
- Covers traditional unit control model + second-generation new energy model (including WECC specification)
- Support PSS/E raw/dyr direct analysis
- Large system simulation performance can reach second level on desktop computers (document example caliber)

### Quote
- H. Cui, F. Li, K. Tomsovic, IEEE TPWRS 2021, DOI: 10.1109/TPWRS.2020.3017019

### License
- GPL v3

## My understanding
- ANDES's "credibility" comes from two lines:
  1) Interpretable symbolic modeling process
  2) Systematic comparison with commercial tools and standard test systems
