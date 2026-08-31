#!/usr/bin/env bash
set -euo pipefail
python scripts/check_results.py
python scripts/reproduce_figures.py
