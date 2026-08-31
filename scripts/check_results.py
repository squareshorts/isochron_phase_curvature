from pathlib import Path
import math
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "data"

settings = pd.read_csv(D / "setting_gains.csv")
agg = pd.read_csv(D / "aggregate_error.csv")
val = pd.read_csv(D / "validation_summary.csv").set_index("quantity")["value"].astype(float)
aff = pd.read_csv(D / "affine_summary.csv").iloc[0]
cov = pd.read_csv(D / "coverage_exceptions.csv")
design = pd.read_csv(D / "benchmark_design.csv").set_index("quantity")["value"].astype(float)
phase = pd.read_csv(D / "phase_assignment_summary.csv").set_index("quantity")["value"].astype(float)

assert len(settings) == 63
assert settings.family.value_counts().to_dict() == {
    "FHN": 18, "ML-II": 11, "ML-I": 7, "HR-fast": 12, "Stuart-Landau": 15
}
assert (settings.gain_eps_010 > 0).all()
assert (settings.gain_eps_025 > 0).all()
assert int(val["fitted_tensors"]) == 63 * 16 == 1008
assert int(design["evaluation_trial_rows"]) == 63 * 16 * 12 * 6 == 72576
assert int(design["fit_sample_rows"]) == 63 * 16 * 16 * 2 == 32256
assert int(design["total_fit_and_evaluation_rows"]) == 104832
assert int(val["invalid_trials"]) == int((cov.total_trials - cov.valid_trials).sum()) == 11

r010 = agg.loc[agg.epsilon.eq(0.10)].iloc[0]
r025 = agg.loc[agg.epsilon.eq(0.25)].iloc[0]
assert math.isclose(r010.reduction_percent, 94.0921, abs_tol=1e-12)
assert math.isclose(r010.reduction_ci_low, 93.0536, abs_tol=1e-12)
assert math.isclose(r010.reduction_ci_high, 95.2774, abs_tol=1e-12)
assert math.isclose(r025.reduction_percent, 83.7562, abs_tol=1e-12)
assert math.isclose(r025.reduction_ci_low, 81.4854, abs_tol=1e-12)
assert math.isclose(r025.reduction_ci_high, 87.7703, abs_tol=1e-12)
assert math.isclose(r025.min_coverage, 186/192, rel_tol=0, abs_tol=5e-7)
assert math.isclose(agg.loc[agg.epsilon.eq(0.20), "min_coverage"].iloc[0], 188/192, rel_tol=0, abs_tol=5e-7)

assert math.isclose(val["first_order_scaling_exponent_median"], 2.0017)
assert math.isclose(val["second_order_scaling_exponent_median"], 3.0255)
assert math.isclose(val["residual_slope_median_eps010"], 0.9980)
assert math.isclose(val["residual_r2_median_eps010"], 0.9834)
assert math.isclose(val["analytic_gradient_max_relative_error"], 2.273e-14)
assert math.isclose(val["analytic_hessian_max_relative_error"], 8.607e-12)

assert int(aff.n_transforms_per_setting) == 250
assert int(aff.n_total_transforms) == 63 * 250 == 15750
assert math.isclose(aff.native_gradient_spread, 7072)
assert math.isclose(aff.native_hessian_spread, 5.508e7)
assert math.isclose(aff.unitbox_gradient_spread, 4.266e5)
assert math.isclose(aff.unitbox_hessian_spread, 2.171e11)
assert math.isclose(aff.worst_whitened_relative_discrepancy, 4.919e-5)

ns = settings.loc[settings.setting_index.eq(29)].iloc[0]
assert ns.family == "ML-I"
assert math.isclose(ns.period, 943.739)
assert math.isclose(ns.gain_eps_010, 75.8)
assert math.isclose(ns.gain_eps_025, 30.6)
assert math.isclose(val["near_snic_residual_slope"], 0.785)
assert math.isclose(val["near_snic_residual_r2"], 0.581)

assert phase["valid_final_distance_max"] < phase["validity_threshold"]
assert phase["invalid_final_distance_min"] > phase["validity_threshold"]

for _, row in agg.iterrows():
    assert row.first_order_error > row.second_order_error > 0
    assert row.reduction_percent > 0

print("PASS: included numerical tables are internally consistent with the reported benchmark summaries.")
