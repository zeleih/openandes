# 09_cases_learning_path

Update time: 2026-03-08 01:44 (Asia/Shanghai)

## 0) This round of verification boundary
- Code repository (local):
  - `andesnotes/repos/andes` (HEAD: `1edce20c`, branch: `master`)
  - `andesnotes/repos/demo` (HEAD: `1a17426`, branch: `master`)
- Only log information that can be verified locally; no conjecture is logged.

## 1) Path overview (order of priority)

### Path A: ANDES built-in case (run through the engine first)
Goal: Confirm that `andes run` is working properly before entering the notebook.

1. Environment preparation (venv + editable install)
2. CLI self-test (`andes --help`)
3. Run `pflow` baseline case (`ieee39.xlsx` recommended)
4. Run `pflow + tds` short-term dynamic (recommended `kundur_full.xlsx`)

**Value**: Fastest verification of "Solver + Data Analysis + Output File".

### Path B: The notebook in the demo warehouse that only relies on ANDES
Goal: Prioritize execution of notebooks that do not depend on `ams` (high success rate).

Priority recommendations (from low threshold to high threshold):
1. `demo/forced_oscillation/forced_oscillation.ipynb`
2. `demo/oscillation/oscillation.ipynb`
3. `demo/interface_andes/interface_andes.ipynb`
4. `demo/misc/*.ipynb` (such as `voltage_sag.ipynb`, `alter_load.ipynb`)

### Path C: AMS benchmark notebook (post-installed)
Goal: Extend to `ams_benchmark/*`.

- This type of notebook explicitly imports ams and `ams` is not detected in the current venv.
- You need to complete the `ltbams/ams` dependency before executing.

## 2) Directory mapping (examples/cases/demo)

### andes warehouse
- Local `examples/` directory not found (no output from `find -name examples`).
- Reproducible examples are mainly located at: `andes/cases/*`
  - Key subdirectories: `ieee14`, `ieee39`, `kundur`, `npcc`, `wecc`, `wscc9`, etc.

### demo warehouse
- The main content is located at: `demo/demo/*`
- A total of **55** `.ipynb` were checked out.
- `README.md` provides navigation entry for advanced usage, simulation, benchmark, and debug.

## 3) Measured and passed vs pending execution

### Passed the actual test
1. `andes` is installable in the local venv and can call the CLI.
2. `andes run andes/cases/ieee39/ieee39.xlsx -r pflow` converges successfully and generates a report.
3. `andes run andes/cases/kundur/kundur_full.xlsx -r pflow tds --tf 0.2` successfully completes the short-term dynamic simulation and outputs `.lst/.npz`.

### To be executed
1. The demo warehouse notebook is automatically executed in batches (it is recommended to run `nbconvert --execute` or run one by one).
2. `ams_benchmark` related notebook (the `ams` dependency needs to be installed and verified first).
3. Special replication of more complete links to `ieee14` (raw+dyr input, perturbation files, etc.).

## 4) Learning promotion suggestions (directly implemented in the next round)
1. First, select 3 ANDES-only notebooks in the demo to do "executable minimum closed loop" (single run + key map/output file confirmation).
2. Create a notebook running matrix (success/failure/missing dependencies/time-consuming).
3. Then enter the AMS benchmark, create a separate environment and record the solver availability (GUROBI/MOSEK/PIQP/pandapower).
