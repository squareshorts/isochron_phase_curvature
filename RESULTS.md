# Benchmark summary

The included numerical tables encode the results reported for the 63-setting benchmark.

- 63 settings: 18 FHN, 11 ML-II, 7 ML-I, 12 HR-fast, and 15 Stuart-Landau.
- 1,008 fitted phase-derivative tensors: 16 phase nodes per setting.
- 72,576 held-out evaluation trials: 16 phase nodes x 12 directions x 6 amplitudes x 63 settings.
- 11 invalid evaluation trials under the final-distance criterion.
- Median first-order residual scaling exponent: 2.0017.
- Median Hessian-corrected residual scaling exponent: 3.0255.
- At epsilon = 0.10, median signed-residual slope: 0.9980; median R^2: 0.9834.
- Median phase-error reduction: 94.0921% at epsilon = 0.10 and 83.7562% at epsilon = 0.25.
- All 63 settings show positive setting-level median error reduction at epsilon = 0.10 and 0.25.
- 250 affine maps per setting, 15,750 transformations total.
- Worst whitened relative descriptor discrepancy: 4.919e-5.

Run `python scripts/check_results.py` to verify these quantities against the included tables.
