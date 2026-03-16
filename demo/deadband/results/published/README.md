# Published Results

This folder stores a small set of representative outputs for the repaired
`deadband` demo so the repository remains lightweight and reviewable.

Included artifacts:

- `day96_agc4_kp0p05_ki0p0625_first/`
  a 96-dispatch day study using the current default AGC settings
- `h13d2_release_compare_current_vs_olddefault_agc4.png`
  a single-dispatch comparison between the current and older AGC defaults
- `h13d2_release_compare_current_vs_olddefault_agc4_summary.csv`
  summary statistics for that `h13d2` comparison
- `h5_pair_boundary_checks/`
  two dispatch-boundary continuity checks for `h5d1 -> h5d2`, including
  cold-stitched vs memory hot-start and cold-stitched vs continuous 1800 s;
  the committed figures are the first `h5` experiment with `KP=0.03`,
  `KI=0.01`

The full working study directories used during development are intentionally not
checked in here.
