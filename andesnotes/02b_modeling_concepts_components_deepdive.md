# ANDES Study Notes - Modeling Concepts & Variables Deep Reading

source:
- `modeling/concepts/framework-overview.html`
- `modeling/concepts/dae-formulation.html`
- `modeling/components/variables.html`

---

## A. Hybrid Symbolic-Numeric Framework

### Core Idea
- Instead of directly handwriting numerical solution code, you first express the model equations and components symbolically.
- The framework autocompletes:
  1) Analyze equation string
  2) Automatic deflection (Jacobian)
  3) Code generation and optimization
  4) vectorized execution

### Value to developers
- Write "physical equations" rather than "derivatives and matrix assembly" details.
- Reuse control blocks (Lag/LeadLag/PI, etc.).
- Reduce model implementation errors through a unified framework.

### Value to users
- Parameters are easier to align with common tools such as PSS/E.
- Running efficiency comes from pre-generated code (`~/.andes/pycode/`).
- There is no need to change the core solver when extending the model.

### Code generation mechanism
- Command: `andes prepare`
- Generated content: equation evaluation functions, Jacobian construction, initialization routines, index maps.
- It will only be regenerated after the model is changed, and the cache will be reused at ordinary times.

---

## B. DAE Formulation

### Mathematical form
- Differential part: `M xdot = f(x, y)`
- Algebraic part: `0 = g(x, y)`

in:
- `x`: state variable (continuous evolution)
- `y`: algebraic variable (instantaneous constraint)
- `M`: mass matrix (usually diagonal)

### Trend vs Transient
- Power flow: Let the derivative be zero and it becomes a purely algebraic equation, solved by NR.
- Transient: time discrete (implicit trapezoidal), each step is transformed into an iteration of nonlinear algebraic equations.

### Jacobi block
- `fx = df/dx`, `fy = df/dy`, `gx = dg/dx`, `gy = dg/dy`
- The framework is automatically constructed without manual derivation.

### Equation writing convention (very important)
- `State`: `e_str` writes the right-hand side `f(...)`, and the left-hand coefficient is provided as `t_const`.
- `Algeb`: must be written as an implicit form with zero residuals (e.g. `x + z - y`), not as a right-hand-side-only expression, otherwise the Jacobian may be singular.

### Initialization method
- Explicit: `v_str`
- Implicit: `v_iter` (iterate to find initial value)

### Discontinuous processing
- Use discrete components (Limiter, etc.) to export status flags (such as at the limit/over the upper limit/over the lower limit), and then splice them into sections in `e_str`.

### Small perturbation linearization
- Linearization at the equilibrium point yields the state matrix `As`, whose eigenvalues ​​determine stability.

---

## C. Variables component (the most basic object for modeling)

### Basic semantics
- A variable is a container of unknown quantities and also contains:
  - `v`: variable value
  - `e`: equation residual value
  - `a`: address in DAE vector (0-based)

### Separation of duties in iteration
- `v` is updated by the solver (the model should not be changed directly).
- `e` is updated from the model equations and summarized for solver iterations.

### Main types
- `State`: Differential state
- `Algeb`: algebraic variables
- `ExtState` / `ExtAlgeb`: referencing external variables across models
- `AliasState` / `AliasAlgeb`: Alias ​​mapping

### State Key Points
- Continuous dynamic variables; time constants/mass coefficients are injected into `dae.Tf` via `t_const`.
- Typical: rotor angle, speed, controller status.

### Algeb Key Points
- Instantaneous constraint variables; equations require implicit residual writing.
- Typical: bus voltage, power balancing, current injection.

### External variable key points
- Used for model coupling (e.g. device access to Bus.v).
- Establish mapping through `model + src + indexer` to avoid manual index hardcoding.

---

## Stage summary
- The essence of ANDES modeling is:
  **Equation declaration (symbolic) + automatic differentiation + automatic code generation + numerical solution**.
- The three most critical disciplines for stable development:
  1) `Algeb.e_str` must be the residual form of "=0";
  2) Put `t_const` on the left side coefficient of `State`, do not mix in `e_str`;
  3) Cross-model coupling gives priority to the `ExtVar` family, and no handwritten address coupling is done.
