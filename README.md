# ISOCHRON - Journal of Nonlinear Science submission package

This package contains the revised ISOCHRON manuscript, Supplemental Material, cover letter, numerical tables, and figure-reproduction script prepared for the Journal of Nonlinear Science.

## Compile in Overleaf

Upload this ZIP as a new Overleaf project. The main manuscript entry point is `main.tex`. The supplementary file is `supplement.tex`; the cover letter is `cover_letter.tex`. The bibliography is in `references.bib`.

The project uses `biblatex` with Biber. Overleaf detects this automatically when `main.tex` or `supplement.tex` is compiled.

## Included numerical material

- `data/aggregate_error.csv`: aggregate phase-reset errors and setting-bootstrap intervals.
- `data/setting_gains.csv`: complete 63-setting gain table.
- `data/coverage_exceptions.csv`: the three setting-amplitude combinations with incomplete coverage.
- `data/validation_summary.csv`: analytic and numerical validation summaries.
- `data/affine_summary.csv`: affine stress-test summary.
- `data/phase_assignment_summary.csv`: final cycle-distance summary.
- `data/benchmark_design.csv`: fit/evaluation row accounting.
- `scripts/check_results.py`: deterministic consistency checks for the numerical quantities reported in the manuscript.
- `scripts/reproduce_figures.py`: regenerates all four figures from the included numerical tables and model equations.

## Windows working copy

Run `setup_local_repo.ps1` after extracting this package. It creates the working copy at:

`C:\work\isochron_phase_curvature`

and initializes a local Git repository on branch `main` when Git is available.
