# 11_runbook_repro_commands

Update time: 2026-03-08 01:44 (Asia/Shanghai)

> Goal: Provide a command chain that can be directly copied and executed, and distinguish between "passed/to be executed".

---

## Command chain 1: Establish ANDES runnable environment (passed actual test)

```bash
cd /Users/hhuhzl/.openclaw/workspace/andesnotes/repos/andes
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip setuptools wheel
python -m pip install -e .
andes --help
```

**Expected Output (Key Snippet)**
- `Successfully installed ... andes-1.10.0.post12+g1edce20cd`
- `usage: andes [-h] ... {run,plot,doc,misc,prepare,prep,selftest,st,demo} ...`

**Common errors and repairs**
1. Error reported: `externally-managed-environment` (PEP 668)
   - Reason: `pip install` directly on the system Python.
   - Fix: Use venv (which is what this command chain does).
2. Error: `command not found: andes`
   - Reason: venv is not activated.
   - Fix: `source .venv/bin/activate` before executing.

---

## Command chain 2: Run power flow baseline case (passed actual measurement)

```bash
cd /Users/hhuhzl/.openclaw/workspace/andesnotes/repos/andes
source .venv/bin/activate
andes run andes/cases/ieee39/ieee39.xlsx -r pflow --no-preamble
```

**Expected Output (Key Snippet)**
- `Parsing input file "andes/cases/ieee39/ieee39.xlsx"...`
- `->Power flow calculation`
- `Converged in 5 iterations`
- `Report saved to "ieee39_out.txt"`

**Common errors and repairs**
1. Error: `error: file "..." does not exist.`
   - Example: `andes/cases/ieee14/ieee14.xlsx` (this file name does not exist in the current warehouse).
   - Fix: First use `find andes/cases -name '*.xlsx'` to confirm the real path.
2. Error: `No module named andes`
   - Fix: Confirmed using `.venv/bin/python` and `.venv/bin/andes`.

---

## Command chain 3: Run short-term dynamic simulation (passed actual measurement)

```bash
cd /Users/hhuhzl/.openclaw/workspace/andesnotes/repos/andes
source .venv/bin/activate
andes run andes/cases/kundur/kundur_full.xlsx -r pflow tds --tf 0.2 --no-preamble
```

**Expected Output (Key Snippet)**
- `Converged in 5 iterations`
- `Initialization for dynamics completed`
- `Simulation to t=0.20 sec completed`
- `Outputs to "kundur_full_out.lst" and "kundur_full_out.npz"`

**Common errors and repairs**
1. Error: Initialization failed (may occur in different cases)
   - Repair: First run `-r pflow` alone; confirm that the working conditions can be converged, and then add `tds`.
2. Error: Simulation time is too long
   - Repair: First shorten `--tf` (such as 0.1~0.5s) for smoke testing.

---

## Command chain 4: demo notebook pre-check (passed actual test)

```bash
python3 - <<'PY'
import json,glob,os,re
root='/Users/hhuhzl/.openclaw/workspace/andesnotes/repos/demo/demo'
paths=sorted(glob.glob(root+'/**/*.ipynb',recursive=True))
print('count', len(paths))
for p in paths[:12]:
    nb=json.load(open(p))
    ks=nb.get('metadata',{}).get('kernelspec',{}).get('name')
    imports=[]
    for c in nb.get('cells',[])[:8]:
        if c.get('cell_type')=='code':
            src=''.join(c.get('source',[]))
            for m in re.findall(r'^\s*(?:import|from)\s+([a-zA-Z0-9_\.]+)',src,flags=re.M):
                imports.append(m.split('.')[0])
    print(os.path.relpath(p,os.path.dirname(root)), 'kernel=',ks,'imports=',sorted(set(imports))[:8])
PY
```

**Expected Output (Key Snippet)**
- `count 55`
- Several lines `... kernel= python3 imports= [...]`

**Common errors and repairs**
1. Error: `JSONDecodeError`
   - Repair: The notebook may be damaged; replace it with a file to verify and locate the damaged file separately.
2. Error: The path is empty
   - Fix: Confirm that the repository has been cloned into `andesnotes/repos/demo`.

---

## Command chain to be executed (not tested yet)

### A) Execute a single ANDES-only notebook
```bash
cd /Users/hhuhzl/.openclaw/workspace/andesnotes/repos/demo/demo/forced_oscillation
# Choose one: jupyter lab / jupyter notebook
jupyter lab
```
- Note: The notebook UI execution was not tested in this round; only the structure and code inspection was completed.

### B) Execute benchmark notebook after AMS dependency check
```bash
# In the target environment
python -c "import ams; print(ams.__version__)"
```
- Note: `ams` cannot be imported under current andes venv; dependencies need to be completed first (refer to demo/environment.yml and ams_benchmark/README.md).

---

## Additional verification records (tested)

```bash
cd /Users/hhuhzl/.openclaw/workspace/andesnotes/repos/andes
source .venv/bin/activate
andes demo
```

- Actual result: `NotImplementedError: Demos have not been implemented`
- Conclusion: `andes demo` is not the available demo entry for the current version. You should use `andes run` or the demo warehouse notebook instead.
