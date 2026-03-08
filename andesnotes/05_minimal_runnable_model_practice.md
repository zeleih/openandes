# ANDES practical operation: minimum runnable custom model (verifiable solution)

> Goal: Based on the learned `creating-models` route, provide a set of minimal custom model practice processes that can be directly executed and verified step by step.
> Constraints: This article does not fabricate running results; only records verified facts + executable commands on this machine.

---

## 1. Goal

Complete a "minimum runnable custom model" closed loop:
1. Prepare the ANDES environment;
2. Copy a custom model based on the official static model example (Shunt);
3. Register the model and execute `andes prepare -i`;
4. Verify that "the model has been recognized by the framework and can generate numerical code" through the command;
5. Provide failure troubleshooting paths.

---

## 2. Preconditions

- macOS/Linux shell
- Python 3.10+ (3.11 recommended)
- `git`
- Accessible on PyPI/GitHub

It is recommended to execute in a separate directory:
```bash
mkdir -p ~/work/andes-dev && cd ~/work/andes-dev
```

---

## 3. Current status of this machine (tested)

The following commands have been executed on the current machine:

```bash
which andes
andes --version
python3 -c "import andes,sys;print(andes.__version__)"
```

Real results obtained:
- `andes` command does not exist (`command not found`)
- Python has no `andes` module (`ModuleNotFoundError: No module named 'andes'`)

Conclusion: ANDES is not installed in your current environment, so the "steps from scratch + verification commands" are provided below.

---

## 4. Practical steps (from zero to verifiable)

## Step A: Create a virtual environment and install ANDES

```bash
cd ~/work/andes-dev
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip setuptools wheel
pip install andes
andes --version
python -c "import andes; print(andes.__version__)"
```

### Expected output
- `andes --version` output version number (such as `1.x.x`)
- Python prints the same version number

---

## Step B: Obtain source code (for custom model development)

```bash
cd ~/work/andes-dev
git clone https://github.com/CURENT/andes.git
cd andes
```

Confirm that official examples exist (avoid path guessing):
```bash
rg -n "class Shunt" andes/models
rg -n "creating-models|example-static|Shunt" docs -S
```

### Expected output
- At least hit the `Shunt` class definition location
- Static model example related pages/text can be retrieved in docs

---

## Step C: Copy the official minimum static model into a custom model

> Principle: Reuse the official minimum viable template first, then change the name and register to reduce the first-round failure rate.

1) Open the `Shunt` source file (use the real path output by `rg` in the previous step).
2) Copy as a new file, for example:
```bash
cp andes/models/shunt.py andes/models/shuntlite.py
```
3) Minimal changes in `shuntlite.py`:
- Change the class name to a unique new name (such as `ShuntLiteData`, `ShuntLite`)
- Keep the equation structure and variable definitions unchanged (don’t change the equation in the first round)
- The model name/docstring is changed to a new name (for easier retrieval)

It is recommended to do a static check after making the changes:
```bash
rg -n "class ShuntLite|ShuntLiteData" andes/models/shuntlite.py
python -m py_compile andes/models/shuntlite.py
```

### Expected output
- `rg` can hit new class names
- `py_compile` no syntax errors

---

## Step D: Register the model and prepare for code generation

1) Edit `andes/models/__init__.py` and add the `ShuntLite` module to the import/registration list (add it according to the existing style of the file).
2) Prepare to perform code generation:
```bash
andes prepare -i
```

### Expected output
- `prepare` process ends and exits without exception
- If there is cache/generation log, import error / attribute error / duplicate model name should not appear

---

## Step E: Minimal "runnable" verification

### E1. Structure verification (required)
```bash
python - <<'PY'
import andes
from andes.system import System
print('andes version:', andes.__version__)
# Only verify package importability and System construction
sys = System()
print('system init ok')
PY
```

### E2. Custom model discoverable verification (required)
> Use `rg` + import double verification to avoid "file exists but not registered".

```bash
rg -n "ShuntLite" andes/models/__init__.py andes/models/shuntlite.py
python - <<'PY'
# If the registration path differs, adjust import statements to your local path
from andes.models.shuntlite import ShuntLite
print('ShuntLite import ok:', ShuntLite.__name__)
PY
```

### E3. Regression run verification (recommended)
> Run the trend using the official built-in case to confirm that the new model does not destroy the basic operating link.

```bash
python - <<'PY'
import andes
ss = andes.load(andes.get_case('ieee14/ieee14_pvd1.xlsx'))
ss.PFlow.run()
print('PFlow exit:', ss.PFlow.exit_code)
PY
```

### Expected output
- Both E1/E2 can print `ok`
- E3 outputs `PFlow exit: 0` (if the sample names are different, please first `python -c "import andes; print(andes.get_case.__doc__)"` or retrieve available cases)

---

## 5. Failure troubleshooting

### Question 1: `andes: command not found`
- Reason: venv is not installed or activated
- Troubleshooting: `which python && which andes`
- Solution: Re-source .venv/bin/activate`, and then `pip install andes`

### Problem 2: `ModuleNotFoundError: andes`
- Reason: The interpreter is not venv's Python
- Troubleshooting: `python -c "import sys; print(sys.executable)"`
- Treatment: Confirm that the path is at `.../.venv/bin/python`

### Question 3: `andes prepare -i` reports import/registration error
- Common reasons:
  - New class name conflicts with existing model
  - `__init__.py` is not registered correctly
  - The class name is inconsistent with the file name after copying
- Troubleshooting commands:
```bash
rg -n "ShuntLite|class .*Data|class .*\(" andes/models/shuntlite.py andes/models/__init__.py
```

### Problem 4: Regression case name does not exist
- Troubleshooting:
```bash
python - <<'PY'
import andes, pkgutil
print('andes imported ok:', andes.__version__)
PY
```
- Solution: Use the official sample that actually exists locally; first confirm that `andes.get_case(...)` can be parsed.

---

## 6. Delivery Criteria (Pass/Fail)

Passing conditions (all met):
1. `andes --version` and Python import both succeed;
2. `shuntlite.py` is compilable;
3. `andes prepare -i` succeeded;
4. `from andes.models.shuntlite import ShuntLite` succeeded;
5. At least one official case of `PFlow.exit_code == 0` (recommended).

Failure condition (any trigger):
- An exception with unidentified cause occurs at any step;
- Just "File created successfully" but import/prepare verification not done.

---

## 7. Remarks

- This article is a "minimum runnable" solution and deliberately does not introduce new equations/discrete logic in the first round.
- Next step suggestion: Change only one controllable parameter in `ShuntLite` (such as adding a new multiplication factor), and repeat the E1~E3 verification link for each change.
