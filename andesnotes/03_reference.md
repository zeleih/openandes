# ANDES Study Notes - Reference

source:
- `reference/index.html`
- `reference/cli.html`
- `reference/configuration.html`

## Reference overall structure
- Command Line Interface
- Configuration
- Model Reference (a large number of model pages)
- Config Reference
- API reference
- Release notes

---

## CLI Key Points

### Command Overview
- `andes run`: run simulation
- `andes plot`: Plot time domain results
- `andes doc`: Query model/routine documentation
- `andes prepare`: generate numerical code from symbolic models
- `andes selftest`: installation verification
- `andes misc`: miscellaneous tools

### run commonly used
- Default flow: `andes run case.xlsx`
- Time domain: `andes run case.xlsx -r tds`
- Characteristic value: `andes run case.xlsx -r eig`
- PSS/E: `andes run system.raw --addfile system.dyr -r tds`
- Configuration injection: `-O Section.option=value`
- Parallel batch: `andes run *.xlsx -r tds --ncpu 4`

### plot commonly used
- `andes plot case_out.lst 0 5`
- Supports variable scope, search by name, export to CSV.

### other
- `andes prepare -f/-i/-q`
- `andes selftest -q`
- `andes misc --edit-config`, `-C` clean output

### Running noise control
- `-v 10/20/30/40` (DEBUG/INFO/WARNING/ERROR)
- Environment variables:
  - `ANDES_USE_UMFPACK`
  - `ANDES_DISABLE_NUMBA`

---

## Configuration key points

### Three-layer configuration
- System: global
- Routine: Analysis routine level (PFlow/TDS/EIG)
- Model: model level (such as TGOV1)

### Configuration view
- `ss.config`
- `ss.PFlow.config`
- `ss.TDS.config`
- `ss.TGOV1.config`

### Configure modification path
1. Python rewrite before running
2. `andes.run(..., config_option=[...])`
3. CLI `-O`
4. Persistence `~/.andes/andes.rc` (`andes --save-config`)

### Common options (the document gives default values)
- System: `freq=60`, `mva=100`, `numba=1`
- PFlow: `tol=1e-6`, `max_iter=25`, `sparselib=klu`
- TDS: `tf=20`, `tstep=1/30`, `fixt=1`, `max_iter=15`, `tol=1e-6`

### Sparse solver
- Recommended KLU (default), can switch to UMFPACK / KVXOPT.

### Automatic adjustment of limits
- `allow_adjust`, `adjust_lower`, `adjust_upper`
- Officials emphasized that the simulation can be guaranteed to continue, but data quality issues may be masked.

## My understanding
- ANDES's CLI and configuration system are very engineering and suitable for "scripted batch research + reproducible experiments".
- It is recommended to fix the template in the future: `run + -O + output directory + log level`.
