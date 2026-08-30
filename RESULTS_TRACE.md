# Numerical results trace

The empirical quantities reported in `main.tex` are linked to the included numerical tables as follows.

| Manuscript result | Source in this package |
|---|---|
| 63 settings; 48 neuronal and 15 Stuart-Landau settings | `data/setting_gains.csv`, family counts; `data/validation_summary.csv` |
| 16 phase nodes and 1,008 fitted tensors | `data/validation_summary.csv`; 63 x 16 = 1,008 |
| 72,576 held-out evaluation trials | `data/benchmark_design.csv`; 63 x 16 x 12 x 6 = 72,576 |
| 104,832 fit-plus-evaluation rows | `data/benchmark_design.csv`; 32,256 local-fit + 72,576 evaluation |
| 11 invalid trials and corrected coverage values | `data/coverage_exceptions.csv`; deficits 4 + 6 + 1 = 11 |
| 94.0921% reduction at epsilon 0.10 and bootstrap interval | `data/aggregate_error.csv` |
| 83.7562% reduction at epsilon 0.25 and bootstrap interval | `data/aggregate_error.csv` |
| Positive improvement in all 63 settings at epsilon 0.10 and 0.25 | every row of `data/setting_gains.csv` has positive `gain_eps_010` and `gain_eps_025` |
| Scaling exponents 2.0017 and 3.0255 with intervals | `data/validation_summary.csv` |
| Signed-residual slope 0.9980 and median R^2 0.9834 with intervals | `data/validation_summary.csv` |
| Analytic gradient and Hessian validation | `data/validation_summary.csv` |
| Halved-step, fit-radius, and phase-subsampling sensitivity | `data/validation_summary.csv` |
| Native/unit-box affine spreads and whitened discrepancy | `data/affine_summary.csv` |
| Near-SNIC ML-I boundary result | setting 29 in `data/setting_gains.csv` and `data/validation_summary.csv` |
| Final-distance validity threshold and accepted/invalid distance ranges | `data/phase_assignment_summary.csv` |

Run `python scripts/check_results.py` to execute the consistency checks used for this package.
