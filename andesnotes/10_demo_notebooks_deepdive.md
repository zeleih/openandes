# 10_demo_notebooks_deepdive

Update time: 2026-03-08 01:44 (Asia/Shanghai)

## 1) Inventory results (verifiable)
- Scan path: `andesnotes/repos/demo/demo/**/*.ipynb`
- Number of notebooks: **55**
- kernelspec: samples are all `python3`

## 2) Dependency layering (by import)

### A. ANDES main line (executed first)
Typical features: `import andes` (often accompanied by `matplotlib`)

Representative documents:
- `demo/forced_oscillation/forced_oscillation.ipynb`
- `demo/oscillation/oscillation.ipynb`
- `demo/interface_andes/interface_andes.ipynb`
- `demo/TGOV1/TGOV1_variants.ipynb`
- `demo/misc/alter_load.ipynb`
- `demo/misc/voltage_sag.ipynb`

Observed code pattern (from notebook code unit):
- `case = andes.get_case('kundur/kundur_full.xlsx')`
- `andes.load(..., pert='./pert.py')`
- `!andes misc --version`

### B. AMS extension cable (rear)
Typical features: `import ams`

Representative documents:
- `demo/ams_benchmark/opf/bench_opf.ipynb`
- `demo/ams_benchmark/opf/bench_opf_repeat.ipynb`
- `demo/ams_benchmark/opf/bench_educ.ipynb`
- `demo/ams_benchmark/UCCase/*.ipynb`

Observed code patterns:
- `import ams`
- `%run ../benchmarks.py`
- Comparison of multiple solvers (GUROBI/MOSEK/PIQP/pandapower)

## 3) Alignment with README
- The navigation of `demo/README.md` is consistent with the directory structure (Advanced Usage / Simulations / Benchmark / Debug).
- `demo/ams_benchmark/README.md` clearly explains the benchmark environment and tool version.

## 4) Current reproducibility judgment

### Passed the actual test (environmental side)
- A venv has been created in the `andes` repository and the `andes` editable installation has been completed.
- Check in this venv that: `andes` is importable, `ams` is not importable (`find_spec('ams') == False`).

### To be executed (notebook side)
- The demo notebooks have not been executed one by one yet (only structure and code unit verification has been completed in this round).
- AMS line notebooks will be executed after dependencies are completed.

## 5) Recommended execution order (minimum risk)
1. `forced_oscillation` → 2) `oscillation` → 3) `interface_andes`
2. Then run `misc/*` mid lane case notebook
3. Finally enter `ams_benchmark/*`

## 6) Risk points identified
- The `andes demo` subcommand currently throws `NotImplementedError: Demos have not been implemented` and is not used as a notebook entry.
- In some cases, the path name is easily written incorrectly (for example, `ieee14.xlsx` does not exist in the current warehouse).
