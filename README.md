# ISOCHRON phase curvature

Supporting numerical data and figure-reproduction code for the manuscript **“Affine-invariant isochron curvature predicts finite-amplitude phase-reduction error in nonlinear oscillators.”**

The study tests whether local asymptotic-phase curvature predicts the finite-amplitude error of first-order phase reduction after covariance whitening. The benchmark contains 63 planar oscillator settings: 18 FitzHugh-Nagumo, 11 Type-II Morris-Lecar, 7 Type-I Morris-Lecar, 12 Hindmarsh-Rose fast-subsystem, and 15 Stuart-Landau settings.

## Contents

- `data/aggregate_error.csv` - aggregate phase-reset errors and bootstrap intervals.
- `data/setting_gains.csv` - complete 63-setting gain table.
- `data/coverage_exceptions.csv` - setting-amplitude combinations with incomplete coverage.
- `data/validation_summary.csv` - derivative, scaling, residual-prediction, and numerical-sensitivity summaries.
- `data/affine_summary.csv` - affine-coordinate stress-test summary.
- `data/phase_assignment_summary.csv` - final cycle-distance summary.
- `data/benchmark_design.csv` - fit/evaluation row accounting.
- `scripts/check_results.py` - consistency checks for the included numerical tables.
- `scripts/reproduce_figures.py` - regenerates the four manuscript figures from the included tables and model equations.
- `figures/` - publication figures in PDF and PNG formats.

## Reproduce the supplied figures

Python 3.10 or later is recommended.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/check_results.py
python scripts/reproduce_figures.py
```

Or run:

```bash
bash run_all.sh
```

## Scope of this release

This repository contains the numerical tables supporting the reported summaries and the code needed to regenerate the four article figures. The data files retain the complete 63-setting results used for the setting-level comparisons and the aggregate numerical validation summaries used in the manuscript.

## Authors

- Thaisse Dias Paes - Signal Processing Laboratory, Institute of Technology, Federal University of Pará, Brazil - ORCID 0009-0006-2429-413X
- Antonio Pereira - Signal Processing Laboratory, Institute of Technology, Federal University of Pará, Brazil - ORCID 0000-0002-0808-1058

## Funding

This work was supported by the Conselho Nacional de Desenvolvimento Cientifico e Tecnologico (CNPq; Grant 309589/2023-1 awarded to Antonio Pereira) and the Coordenacao de Aperfeicoamento de Pessoal de Nivel Superior (CAPES).

## Citation

Please cite the versioned Zenodo archive associated with the GitHub release. Citation metadata are provided in `CITATION.cff`.

## License

Code is released under the MIT License. Numerical data and documentation are released under CC BY 4.0; see `LICENSE-DATA`.
