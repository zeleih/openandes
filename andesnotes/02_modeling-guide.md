# ANDES Study Notes - Modeling Guide

Source: `modeling/index.html`

## position
Modeling Guide for developers:
- Understand the internal modeling mechanisms
- Custom device model
- Extend framework capabilities

## Chapter structure

### 1) Modeling Concepts
- Hybrid Symbolic-Numeric Framework
- Atomic Types
- System Architecture
- DAE Formulation

### 2) Model Components
- Parameters
- Variables
- Services
- Discrete Components
- Blocks
- Groups

### 3) Creating Models
- Model Structure
- Example: Shunt (static model)
- Example: BusFreq (dynamic model)
- Example: TGOV1
- Example: IEEEST
- Testing Models

## My understanding
- This is the "Engine Layer Manual" of ANDES. The core is **Symbolic Modeling -> Automatically Generate Numerical Calculation Code**.
- Maximum value for research users: Avoid manual derivation of the Jacobian and handwritten numerical solution code.
- Value to engineering practice: the model is reusable, testable, and versionable.

## Follow-up intensive reading plan
- Read `framework-overview` and `dae-formulation` first.
- Read the 4 official examples of `creating-models` again to refine the templated development process.
