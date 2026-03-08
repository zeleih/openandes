# ANDES Modeling Cheat Sheet (for minimal custom models)

> Purpose: Quickly check commands and checkpoints when executing/reviewing the "minimum runnable custom model".
> Principle: run through first, then expand; each step must have a verification command.

---

## 1) Goal

- Quickly complete without making up the results: environment available → model copy and rename → registration → prepare → import verification → regression run.

---

## 2) Preconditions

```bash
python3 --version
git --version
```

If ANDES is not installed:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip setuptools wheel
pip install andes
andes --version
python -c "import andes; print(andes.__version__)"
```

---

## 3) Minimum steps (Checklist)

## Step A. Find the official minimal template
```bash
cd ~/work/andes-dev/andes
rg -n "class Shunt" andes/models
```

## Step B. Copy and rename
```bash
cp andes/models/shunt.py andes/models/shuntlite.py
# Manually rename classes: ShuntData/Shunt -> ShuntLiteData/ShuntLite
python -m py_compile andes/models/shuntlite.py
```

## Step C. Register model
```bash
# Validate after editing andes/models/__init__.py
rg -n "ShuntLite" andes/models/__init__.py andes/models/shuntlite.py
```

## Step D. Generate/refresh numerical code
```bash
andes prepare -i
```

## Step E. Runnable verification
```bash
python - <<'PY'
from andes.models.shuntlite import ShuntLite
print('import ok:', ShuntLite.__name__)
PY
```

```bash
python - <<'PY'
import andes
ss = andes.load(andes.get_case('ieee14/ieee14_pvd1.xlsx'))
ss.PFlow.run()
print('PFlow exit:', ss.PFlow.exit_code)
PY
```

---

## 4) Commands and expected output (quick check)

- `andes --version` → output version number
- `python -m py_compile andes/models/shuntlite.py` → no output and exit code 0
- `andes prepare -i` → ends without exception
- `from andes.models.shuntlite import ShuntLite` → print `import ok`
- `PFlow.exit_code` → expected `0`

---

## 5) Common failure troubleshooting

### A. CLI does not exist
```bash
which andes
which python
```
Solution: Activate venv and reinstall.

### B. The module cannot be imported
```bash
python -c "import sys; print(sys.executable)"
python -c "import andes; print(andes.__version__)"
```
Workaround: Make sure to use the same venv interpreter.

### C. prepare failed
```bash
rg -n "ShuntLite|class" andes/models/shuntlite.py andes/models/__init__.py
```
Processing: Check for class name conflicts, registration omissions, and spelling errors.

### D. case path error
Solution: Use the local parsable official case instead, and then verify `PFlow.exit_code`.

---

## 6) Extension suggestions (after passing the minimum solution)

1. Only introduce one new change at a time (choose one of three parameters/equations/discrete logic);
2. Repeat for each change: `py_compile -> prepare -> import -> PFlow`;
3. Record failure logs and repair actions to form a personal modeling regression list.
