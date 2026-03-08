# ANDES manual cross-reference (based on docs-andes-app-en-v2.0-dev.pdf)

Manual information:
- File: `docs-andes-app-en-v2.0-dev.pdf`
- Version identification (cover): `Release 0.0.post50+g7101dce13`
- Number of pages: 1031
- Reading method: local extraction of table of contents and chapter text (pypdf)

## 1) Directory structure and core themes (verification)

- Ch1 About ANDES
- Ch2 Tutorials（2.1~2.16）
  - Chapters seen include: Installation, First Simulation, Power Flow, TDS, Data & File Formats, Plotting, EIG, Parameter Sweeps, Contingency, Dynamic Control, Frequency Response, State Estimation, CPF, Inspecting Equations, RL with ANDES
- Ch3 Modeling Guide（3.1~3.4）
  - Modeling Concepts / Model Components / Creating Models
- Ch4 Reference (CLI/Configuration/Model Reference/Config Reference/API reference)

## 2) Reflection of existing learning results

### A. Covered and consistent with the manual
- Tutorials 02~11 + Inspecting (corresponding to 2.3~2.11, 2.15)
- Modeling Concepts (corresponds to 3.2)
- Components (corresponding to 3.3: Parameters/Variables/Services/Discrete/Blocks/Groups)
- Creating Models core example (corresponding to 3.4.4~3.4.8: Shunt/BusFreq/TGOV1/IEEEST/Testing)
- Reference direction (CLI/Config created notes)

### B. Add confirmation points after comparing with the manual
- Tutorials actually extended to 2.16 (not just to 2.11/2.15)
- Advanced analysis topics are clearly within the main thread of the tutorial:
  - 2.12 Frequency Response and Load Shedding
  - 2.13 State Estimation
  - 2.14 Continuation Power Flow
  - 2.16 Reinforcement Learning with ANDES

## 3) Current note gap (based on manual table of contents facts only)

1. Gaps in the second half of Tutorials: `2.12/2.13/2.14/2.16`. Independent in-depth reading notes have not yet been formed.
2. Reference depth notch:
   - `4.3 Model Reference` (large-scale model family entry)
   - `4.4 Config Reference` (System/PFlow/TDS/EIG/SE/CPF)
   - `4.5 API reference` (System/Routines)
3. Verification layer gap: There is no "actual measurement operation screenshot/log type evidence" to cover the above gap chapter.

## 4) Correction suggestions (executable)

- First supplement Tutorials 2.12~2.14 (close to the power system analysis scenario)
- Added 2.16 (RL) as an extension
- Use "reverse check by task" for Reference instead of full transcription:
  - First do `4.1 CLI` + `4.2 Config` command index
  - Combined with the actual model requirements, drill down to `4.3/4.4/4.5`

## 5) Conclusion

The existing learning results are consistent with the main structure of the manual, and the core link of Creating Models has been closed;
The main gap lies in the systematic coverage of the second half of Tutorials (2.12~2.16) and the Reference deep water area (4.3~4.5).
