# ANDES Study Notes - Creating Models Advanced Examples (BusFreq / TGOV1 / IEEEST)

source:
- `creating-models/example-dynamic`
- `creating-models/example-tgov1`
- `creating-models/example-ieeest`

---

## 1) BusFreq (dynamic measurement model)

### position
- This is a "read-only dynamic model": bus angle/voltage is read, local frequency estimate is output, no power is injected into the network.
- Only participate in TDS: `flags.tds = True`, do not participate in trends.

### Key links
1. `ExtService` captures the initial phase angle `a0` (from the initial value of the power flow)
2. `ExtAlgeb` reads the current phase angle `a`
3. `Lag` versus `(a-a0)` low-pass filtering (anti-noise)
4. `Washout` approximates the derivative and obtains the frequency deviation `WO_y`
5. `Algeb` output `f = 1 + WO_y`

### Key inspiration
- Dynamic models can automatically create internal states through blocks, eliminating the need to hand-write all state equations during development.
- The measurement model commonly uses the structure of “reading external variables + signal chain processing + local output”.

---

## 2) TGOV1 (two implementation paradigms)

### Model structure
- droop + lag (including anti-windup) + lead-lag + damping term Dt.

### A. Equation-based
- Explicitly write `State/Algeb` and `e_str`.
- Advantages: Completely controllable, enabling unconventional structures.
- Disadvantages: long code and high error probability.

### B. Block-based
- Use `LagAntiWindup`, `LeadLag` and other standard blocks for splicing.
- Advantages: high readability, close to the control block diagram, and fast implementation.
- Disadvantages: Constrained by existing block capability boundaries.

### Official practical conclusion
- Performance is basically the same.
- Regular controllers are block-based first; special structures use equation-based or hybrid.

---

## 3) IEEEST (complex PSS example)

### Complexity
- Multi-input mode (speed/frequency/power/acceleration power/voltage/dVdt)
- Multi-stage transfer chain (second-order filter + two-stage lead-lag + gain + washout/lag)
- Limiting and mode switching
- Optional remote busbar

### Key technical parts
1. `Replace`: replace invalid input (such as 0 limit)
2. `DataSelect`: Optional parameter fallback (the remote bus uses the local bus by default)
3. `DeviceFinder`: Find or automatically create associated measurement devices (such as BusFreq)
4. `Switcher`: decode MODE into `SW_s1..SW_s6` flag
5. `Derivative`: Mode 6 requires `dV/dt`
6. `ExtService(attr='pu_coeff')`: conversion coefficient from unit base value to system base value

### Input signal construction method
- Use the `Switcher` flag to do a piecewise weighted sum, activating only the current mode counterpart.
- `v_str` and `e_str` are written separately to improve the readability of initialization and equations.

### Group interface requirements
- The PSS group requires a common output variable `vsout` for unified access to Exciter.

---

## 4) The modeling methodology I refined (can be directly reused)

1. **Determine the interface first, then determine the equation**
- Define Group/common vars and external connections first, and then write internal dynamics.

2. **Run first, then optimize**
- The first version gives priority to block-based verification behavior; then switch to equation-based as needed.

3. **Discrete logic explicit**
- All limiting/switching should be expressed using Discrete components to avoid implicit if-else.

4. **Initialization priority is higher than dynamic details**
- `ExtService`, `v_str`, and initialization residual checking are the keys to preventing crashes.

5. **Complex models must be tested at three levels**
- unit + integration + verification (vs. reference tool).

---

## Current status
- Creating Models Four core examples (Shunt/BusFreq/TGOV1/IEEEST) have been completed.
- The path from entry-level modeling to advanced controller implementation is closed.
