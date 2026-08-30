#!/usr/bin/env bash
set -euo pipefail

python scripts/check_results.py | tee results_check.log
python scripts/reproduce_figures.py | tee figure_reproduction.log
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex | tee main_build.log
latexmk -pdf -interaction=nonstopmode -halt-on-error supplement.tex | tee supplement_build.log
latexmk -pdf -interaction=nonstopmode -halt-on-error cover_letter.tex | tee cover_letter_build.log
