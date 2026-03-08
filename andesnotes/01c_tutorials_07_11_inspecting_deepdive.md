# ANDES Study Notes - Tutorials 07~11 + Inspecting Models Deep Reading

source:
- 07-eigenvalue-analysis
- 08-parameter-sweeps
- 09-contingency-analysis
- 10-dynamic-control
- 11-frequency-response
- inspecting-models

---

## 07 Eigenvalue Analysis (stable with small disturbances)

### Core Process
1. Establish operating point (automatically run the flow first)
2. Linearize to get the state matrix
3. Calculate eigenvalues ​​and count positive/zero/negative roots
4. Explain stability and damping using s-plane diagrams

### Key conclusions
- Real part < 0: stable mode; real part > 0: unstable mode.
- The imaginary part determines the oscillation frequency.
- Zero eigenvalues ​​usually correspond to angular reference degrees of freedom (physically acceptable).

### Engineering capabilities
- `ss.EIG.plot()` looks at the modal distribution.
- `ss.EIG.sweep(param, idx, range)` is used as the root locus, which is directly used to control parameter tuning (such as EXDC2.KA).
- `*_eig.txt` report contains damping ratio, frequency, correlation status.

---

## 08 Parameter Sweeps & Batch Processing

### Three batch paradigms
1. **File batch processing + CLI parallel** (preferred for large-scale research)
   - First generate case files in batches, then `andes run batch/*.xlsx -r tds --ncpu N`.
2. **Python loop memory parameter scanning** (small-scale, quick test)
3. **`pool=True` returns System objects in parallel** (medium scale, requires programmatic post-processing)

### Selection Principle
- >100 scenarios: file parallelism
- Medium: pool=True
- Small sample: single process loop (fastest for development)

### Key understanding
- ANDES's batch processing is not a "incident feature", but a complete experimental pipeline capability.

---

## 09 Contingency Analysis (N-1 and fault clearing)

### Standard process
1. Enumerate components under test (Line/Gen/Bus)
2. Create a new system for each scenario and inject disturbances
3. Run TDS
4. Scored using a unified stability index

### Common indicators
- `omega_max < 1.05`
- `omega_min > 0.95`
- `v_min > 0.8`
- `exit_code == 0`

### CCT (critical resection time)
- The document gives a binary search template and updates the upper and lower bounds according to stability/instability.
- CCT is a core indicator of protection value and system resilience.

---

## 10 Dynamic Control & Setpoint Changes (staged simulation)

### Key mechanisms
- `ss.TDS.run()` can be called multiple times to continue the simulation from the current state.
- The setting value (such as `TGOV1.paux0`) can be modified between two runs to implement AGC/scheduling/control strategy injection.

### Practical Notes
- Parameter array modifications must be written "in-place".
- Control is injected before continuing to the new `tf`.

### Application scenarios
- Economic dispatch tracking
- AGC frequency adjustment
- Voltage set point control
- Reinforcement learning closed-loop control

---

## 11 Frequency Response & Load Shedding

### Research objects
- Frequency drop and recovery after generator trip.
- UFLS (Under Frequency Load Shedding) action effect.

### Key processes
1. Injection generator trip (Toggle)
2. Observe frequency drops (Governor droop creates a new equilibrium below rating)
3. Quantitative estimation of power deficit
4. Load shedding according to strategy in the second stage (modify `PQ.Ppf`)
5. Continue simulation to verify frequency recovery

### Core concepts
- Droop control is not equal-frequency control, and the steady-state frequency after a fault is usually lower than rated.
- If the load shedding is close to the deficit, the frequency can be restored significantly.
- RoCoF is strongly related to system inertia.

---

## Inspecting Model Equations

### Ability entrance
- `ss.supported_models()`: List of models.
- `model.prepare()`: Prepare symbolic equations.
- `model.doc()`: Output the complete model document (parameters, variables, equations, services, configuration).

### Symbol object
- `syms.xy`: variable vector
- `syms.f`: differential equation RHS
- `syms.g`: algebraic equations RHS
- `syms.df`, `syms.dg`: Jacobi
- `syms.s`: service equation

### Actual value
- Verification: Check whether the physical meaning of the model is correct
- Debugging: Locate the source of the abnormal response
- Extensions: Structural baseline before developing new models
- Reporting: Generate citation-ready mathematical expressions

---

## Stage conclusion (Tutorials basically closed loop completed)
- I have upgraded the Tutorials from "Function Usage" to the "Experimental Design + Batch Analysis + Stability Criteria + Equation Review" level.
- Currently it can directly support:
  1) Small perturbation stability study (EIG + root locus)
  2) Large-scale N-1 batch processing
  3) Staged control strategy simulation
  4) Trip and load shedding strategy evaluation
  5) Model-level equation audit
