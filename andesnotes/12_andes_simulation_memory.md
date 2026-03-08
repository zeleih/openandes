# ANDES Simulation Memory (Living File)

> Purpose: keep a continuously updated, practical memory of what works, what fails, and what to check first when running ANDES simulations in this project.

## 1) Verified Stable Workflow

1. Use `python -m andes` in a dedicated virtual environment.
2. Run `pflow` before `tds` (or `-r pflow tds` in one command).
3. For multi-scenario studies (S1–S4 etc.), always isolate outputs by run folder.
4. Keep perturbation logic in standalone script files under `simulations/<run>/scripts/`.
5. Generate plots from saved outputs (`.lst` + `.npz`) after all runs finish.

## 2) Important Command Notes

- Version check should use:
  - `python -m andes misc --version`
- Do not rely on:
  - `andes --version` (not valid in this workflow)

## 3) Core Engineering Findings

### 3.1 Deadband Modeling
- `TGOV1NDB dbL/dbU` are per-unit deadband parameters.
- Frequency-domain interpretation requires proper scaling (commonly x60 for Hz interpretation).

### 3.2 PVD2 / ESD2 Caveats
- `PVD2 fdbd` uses named-value style and can require sign convention handling.
- `ddn` acts as post-deadband gain.
- `ESD2` sheet may exist in case files while runtime still logs:
  - `<ESD2> is not an existing model`
- Conclusion: table presence != active model loading; branch/version alignment is mandatory.

### 3.3 Output Integrity Rule
- A previous false conclusion was caused by reading stale files with same output names.
- Mandatory fix: each run must write to dedicated `-o run_dir`.

## 4) Current Reproducible Test Pattern (IL200)

- System: Illinois 200-bus dynamic cases (four settings S1–S4)
- Simulation horizon: 50 s
- Disturbance: permanent load increase at 5 s
- Output: frequency comparison curve + JSON summary

## 5) Debug Checklist (Order Matters)

1. Environment
   - Correct Python interpreter / ANDES import works
2. Case parsing
   - No missing model class errors beyond known limitations
3. Initialization
   - PFlow converges before TDS starts
4. Event trigger
   - Perturbation log confirms event time and target
5. Output sanity
   - Check minima/trends across scenarios
6. Path hygiene
   - Ensure plot scripts read current run outputs only

## 6) Update Protocol (Keep This File Alive)

After each meaningful simulation session, append one entry under **Session Log** using this template:

```markdown
### YYYY-MM-DD HH:MM (TZ)
- Goal:
- Cases/Scenarios:
- Environment:
- What worked:
- What failed:
- Root cause:
- Fix applied:
- Repro command(s):
- Result summary:
- Follow-up action:
```

Maintenance rules:
- Keep facts only (no guesses).
- Keep command snippets executable.
- Keep failure -> cause -> fix chain explicit.
- If a prior rule is invalidated, update the rule text directly and mark the old one as deprecated.

---

## 7) Session Log

### 2026-03-08 14:00 (Asia/Shanghai)
- Goal: rebuild a clean simulation folder and rerun 4-setting IL200 frequency comparison.
- Cases/Scenarios: `IL200_dyn_db_opt_S1..S4`.
- Environment: Python in `.envs/.venv-andes312`, `python -m andes` CLI.
- What worked:
  - 50 s runs completed for all S1–S4.
  - Event at 5 s triggered by perturbation script.
  - Frequency comparison plot generated successfully.
- What failed:
  - An initial perturbation implementation produced flat frequency results.
- Root cause:
  - Load update path was ineffective for this case configuration.
- Fix applied:
  - Switched to `Req/Xeq` step-change style perturbation at 5 s.
- Repro command(s):
  - see `simulations/test/README.md`
- Result summary:
  - S1–S4 produced differentiated nadir values and expected ordering.
- Follow-up action:
  - keep this pattern as baseline for future comparative studies.
