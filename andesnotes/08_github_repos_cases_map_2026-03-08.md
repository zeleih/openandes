# ANDES GitHub + Demo warehouse learning record (2026-03-08)

## 1) Warehouse synchronization
- ANDES source code repository: `andesnotes/repos/andes`
- Demo repository: `andesnotes/repos/demo`

## 2) Case / Demo resource inventory (key points)

### ANDES built-in case (`andes/andes/cases`)
- Typical systems: `ieee14`, `ieee39`, `kundur`, `wecc`, `npcc`, `wscc9`, `nordic44`, `GBnetwork`, `matpower`, `5bus`, `smib`, etc.
- File form: `.xlsx`, `.json`, `.raw`, `.dyr`, `.m`, etc. mixed.
- The `ieee14` subdirectory contains a large number of controller/disturbance/fault examples (e.g. `fault`, `linetrip`, `gentrip`, `pllvfu1`, `esst*`, `hygov*`).

### demo warehouse (`demo/demo/*`)
- Simulation classes: `forced_oscillation`, `oscillation`, `freq_response`, `TGOV1`, `TurbineGov_response`, `bus_current_injection`, `andes_stochastic`
- System level: `texas7k`, `hawaii`, `rolling_horizon`
- Debugging and skills: `misc` (including `output_select`, `alter_load`, `voltage_sag`, `andes_tds_init`, `busfreq`, etc.)
- benchmark: `pflow_benchmark`

## 3) Operating environment installation and actual testing

### environment
- `/.venv-andes` (Python 3.14) ANDES is installed, but there are compatibility issues when running case.
- Create new `/.venv-andes312` (Python 3.12.13) and install ANDES 1.10.0.

### Key commands and results
1. version check
- `andes misc --version` ✅
- Explanation: `andes --version` is not a valid argument.

2. Numerical code generation
- `andes prepare -q` ✅
- Generation path: `~/.andes/pycode`

3. Basic case verification
- Python API: `andes.load(andes.get_case('ieee14/ieee14.json')); ss.PFlow.run()` ✅ `PFlow converged True`

4. demo case verification
- Order:
  `andes run .../demo/TGOV1/ieee39_TGOV1.xlsx -r pflow`
- Result: NR converges after 5 iterations, output `ieee39_TGOV1_out.txt` ✅

## 4) Current learning conclusion
- The "case learning path" in the GitHub repository can be implemented (PFlow can run through the built-in case and demo case).
- Follow-up highlights:
  1) Learn the notebook structure of the demo one by one (input, perturbation script, output analysis);
  2) Make `TGOV1 / forced_oscillation / freq_response` into reproducible practice notes;
  3) Establish a "chapter-example mapping table" in the ANDES main repository by comparing `cases` and document chapters.
