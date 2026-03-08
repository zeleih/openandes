# ANDES Study Notes - Components + Creating Models Deep Reading (this round)

source:
- modeling/components/{parameters, services, discrete, blocks, groups}
- modeling/creating-models/model-structure
- modeling/creating-models/example-static
- modeling/creating-models/testing-models

---

## 1) Parameters (parameter system)

### Core Cognition
- The argument is `v-provider`, which is used to provide values ​​to the equation.
- Common types:
  - `NumParam`: Numeric parameter (default value/constraint/TeX available)
  - `IdxParam`: Index parameter (cross-model reference entry)
  - and external parameters `ExtParam` (get other model parameters through group/indexer)

### Engineering significance
- Parameter definition is the core of model portability: input data, units, and constraints are unified.
- Constraints such as `mandatory=True` and `non_zero=True` can expose data problems in advance.

---

## 2) Services (service system)

### Core Cognition
- Service is the "intermediate calculation layer" and is not directly solved as unknown variables.
- common:
  - `ConstService`: constant expression
  - `VarService`: dynamic update of dependent variables
  - `BackRef`: reverse connection relationship (for example, Bus collects the idx list of attached devices)

### Engineering significance
- Split complex equations into "readable intermediate terms + final equation" to facilitate debugging and auditing.

---

## 3) Discrete Components

### Core Cognition
- Discrete components are used for segmented logic/limiting/compare/switching.
- Typical export flags:
  - `Limiter` exports `zi/zl/zu` (in bounds/lower/upper)
- Update timing is very critical:
  - `check_var`: Update variable class flag before equation evaluation
  - `check_eq`: Update equation class flag after equation evaluation
  - `set_var`: write back after solution (such as AntiWindup state clamp)

### High value components
- `Limiter`, `HardLimiter`, `SortedLimiter`
- `RateLimiter`, `AntiWindup`, `AntiWindupRate`
- `LessThan`, `Switcher`, `DeadBand`, `Delay`, `Sampling`

### Practical discipline
- For piecewise equations, use flag to spell `e_str`, and do not write loose if-else logic.
- To overlay RateLimiter and AntiWindup, use the combined version (AntiWindupRate) as recommended by the documentation.

---

## 4) Blocks (control building blocks)

### Core Cognition
- Block is a reusable subsystem of "predefined variables + equations" (similar to a control module library).
- All exported elements must be registered to `self.vars`.
- Nesting is possible, but the official recommendation is not to exceed 1 level to avoid naming expansion.

### Typical block family
- Linear transfer: `Gain`, `Lag`, `Washout`, `LeadLag`, `Lag2ndOrd`
- Contains constraints: `GainLimiter`, `LagAntiWindup`, `LagRate`, `LeadLagLimit`
- Controllers: `PIController`, `PIDController`, tracking/anti-windup/freeze variants
- Non-linear gating: `HVGate`, `LVGate`, `Piecewise`, `DeadBand1`

### Naming mechanism (key)
- Parent block name + child block name + variable name concatenation (such as `A_B_x`), automatically propagated by the framework.
- You must use the runtime final name pattern (`{self.name}_v`) when writing `define()`.

---

## 5) Groups (grouping and polymorphic interface)

### Core Cognition
- Group is "a unified interface contract for similar models".
- effect:
  - Public parameter/variable interface
  - Model polymorphic substitution (such as GENCLS ↔ GENROU)
  - Cross-model reference compatibility
  - Reverse connection query (BackRef)

### Typical standard group
- `StaticGen`, `SynGen`, `Exciter`, `TurbineGov`, `PSS`, `StaticLoad`, `RenGen`, etc.

### GroupBase common capabilities
- `add_model`, `add`, `get`, `set`, `alter`, `find_idx`, `idx2model`, `idx2uid`, `doc_all`.

### Practical value
- Through the group + indexer design, it is possible to "replace the model without changing the case file".

---

## 6) Creating Models - Model Structure (modeling skeleton)

### Standard two categories
1. `ModelData`: parameter definition
2. `Model`: behavior definition (flags/group/service/var/equation)

### Recommended component order
1) flags/group → 2) config → 3) const/ext services → 4) ext params/vars → 5) var services → 6) discrete/blocks → 7) Algeb/State

### flags
- `pflow`, `tds`, `tds_init` determine the analysis process involved.

### Registration and code generation
- Models are added to `andes/models/__init__.py`.
- After modification, execute: `andes prepare -i`.

---

## 7) Example: Static Model (Shunt)

### Key points learned
- Static models only provide algebraic equations and do not contain state variables.
- `Shunt` uses `ExtAlgeb` to hook directly to `Bus.a / Bus.v`.
- The equation reflects the constant impedance characteristic:
  - `P = V^2 g`
  - `Q = -V^2 b`
- `y=True` parameter annotation is related to the admittance matrix, which is beneficial to sparse solution.

### Key inspiration
- This is the clearest "Data/Model separation + external variable injection + algebraic injection" template.

---

## 8) Testing Models (Testing System)

### Three-tier testing
1. Unit: can be instantiated, parameters can be read
2. Integration: The power flow/transient state in the system can run
3. Verification: Comparison with reference tools such as PSS/E

### Must-do use cases
- PFlow convergence
- TDS flat running without drifting
- After perturbation `exit_code==0`
- Initialization residual `f/g` is small enough
- Boundary checking of key variables (such as frequency, voltage)

### Debugging tool chain
- Look at `dae.f/dae.g` residuals
- Look at Jacobian sparse graphs (`spy(gy)`)
- Reduce step size + shorten simulation window + DEBUG log

---

## Stage summary
- I have basically opened up the "modeling platform" of ANDES:
  **Parameters/Services/Discrete/Block/Group/Skeleton/Test** Set of seven.
- The next stage will complete the refinement points of the remaining example pages of Creating Models:
  - Dynamic (BusFreq)
  - TGOV1
  - IEEEST
(In this round, tabs are lost in some page snapshots, and single pages will be reopened later to make up for them)
