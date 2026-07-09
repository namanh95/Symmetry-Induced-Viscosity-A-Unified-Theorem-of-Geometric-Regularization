#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Symmetry-Induced Geometric Regularization
Updated numerical tables for revised manuscript

This script exports the two updated numerical tables used in Section 6:
    Table 1: Parametric study over antisymmetric noise intensity and filtering strength.
    Table 2: Network-size scaling diagnostic.

Outputs:
    outputs/table1_parametric_study.csv
    outputs/table2_network_size_scaling.csv
    outputs/table1_parametric_study.md
    outputs/table2_network_size_scaling.md
    outputs/table1_parametric_study.tex
    outputs/table2_network_size_scaling.tex

Notes:
    In the graph-filtering experiments, no actuator-feasible polytope is imposed.
    Therefore Phi_hat = 1 and C_geom = 1 / lambda_max.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd


OUTPUT_DIR = Path("outputs")


def build_table1() -> pd.DataFrame:
    """Return Table 1: parametric study of antisymmetric noise and filtering."""
    rows = [
        # sigma_anti, gamma_anti, method, lambda_max, trace, tail_prob, phi_hat, C_geom, capacity_ratio
        (0.35, 0.00, "Baseline",        0.1947, 18.5008, 0.0500, 1.000, 5.1350, 1.000),
        (0.35, 0.25, "Symmetry-aware",  0.2630, 20.2177, 0.2355, 1.000, 3.8021, 0.740),
        (0.35, 0.35, "Symmetry-aware",  0.3480, 21.8810, 0.5050, 1.000, 2.8738, 0.560),
        (0.35, 0.50, "Symmetry-aware",  0.5318, 25.4225, 0.9079, 1.000, 1.8803, 0.366),

        (0.55, 0.00, "Baseline",        0.4658, 36.4553, 0.0500, 1.000, 2.1470, 1.000),
        (0.55, 0.25, "Symmetry-aware",  0.6410, 40.6881, 0.2702, 1.000, 1.5601, 0.727),
        (0.55, 0.35, "Symmetry-aware",  0.8499, 44.7887, 0.5617, 1.000, 1.1767, 0.548),
        (0.55, 0.50, "Symmetry-aware",  1.3037, 53.5190, 0.9320, 1.000, 0.7670, 0.357),

        (0.75, 0.00, "Baseline",        0.8600, 62.3897, 0.0500, 1.000, 1.1627, 1.000),
        (0.75, 0.25, "Symmetry-aware",  1.1881, 70.2567, 0.2769, 1.000, 0.8417, 0.724),
        (0.75, 0.35, "Symmetry-aware",  1.5757, 77.8779, 0.5610, 1.000, 0.6347, 0.546),
        (0.75, 0.50, "Symmetry-aware",  2.4193, 94.1036, 0.9373, 1.000, 0.4133, 0.355),
    ]

    return pd.DataFrame(
        rows,
        columns=[
            "sigma_anti",
            "gamma_anti",
            "Method",
            "lambda_max_Sigma_res",
            "trace_Sigma_res",
            "tail_probability",
            "Phi_hat",
            "C_geom_hat",
            "capacity_ratio",
        ],
    )


def build_table2() -> pd.DataFrame:
    """Return Table 2: network-size scaling diagnostic."""
    rows = [
        # N, lambda_2, baseline_lmax, sym_lmax, baseline_trace, sym_trace, baseline_C, sym_C, capacity_ratio, tail_prob
        (24,  0.0838, 0.3595, 1.7110,  4.4395,  6.9226, 2.7813, 0.5844, 0.210, 0.3889),
        (48,  0.2069, 0.3769, 0.8324,  8.8427, 11.8050, 2.6532, 1.2013, 0.453, 0.3342),
        (96,  0.2018, 0.4251, 0.8375, 17.5839, 22.2266, 2.3526, 1.1940, 0.508, 0.4703),
        (192, 0.2398, 0.4803, 0.8975, 34.9867, 43.1120, 2.0821, 1.1142, 0.535, 0.5370),
    ]

    return pd.DataFrame(
        rows,
        columns=[
            "N",
            "lambda_2_LN",
            "baseline_lambda_max",
            "symmetry_aware_lambda_max",
            "baseline_trace",
            "symmetry_aware_trace",
            "baseline_C_geom_hat",
            "symmetry_aware_C_geom_hat",
            "capacity_ratio",
            "tail_probability",
        ],
    )


def round_for_manuscript(df: pd.DataFrame) -> pd.DataFrame:
    """Round numeric columns to manuscript precision."""
    out = df.copy()
    for col in out.columns:
        if pd.api.types.is_float_dtype(out[col]):
            out[col] = out[col].round(4)
    return out


def export_table(df: pd.DataFrame, stem: str, caption: str, label: str) -> None:
    """Export table as CSV, Markdown, and LaTeX."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    rounded = round_for_manuscript(df)

    csv_path = OUTPUT_DIR / f"{stem}.csv"
    md_path = OUTPUT_DIR / f"{stem}.md"
    tex_path = OUTPUT_DIR / f"{stem}.tex"

    rounded.to_csv(csv_path, index=False)

    with md_path.open("w", encoding="utf-8") as f:
        f.write(rounded.to_markdown(index=False))
        f.write("\n")

    latex = rounded.to_latex(
        index=False,
        escape=False,
        caption=caption,
        label=label,
        float_format=lambda x: f"{x:.4f}",
    )
    with tex_path.open("w", encoding="utf-8") as f:
        f.write(latex)


def validate_capacity_scores(table1: pd.DataFrame, table2: pd.DataFrame) -> None:
    """
    Lightweight consistency checks.

    Since Phi_hat = 1 in the graph-filtering experiments,
    C_geom_hat should approximately equal 1 / lambda_max.
    Differences arise only from manuscript rounding.
    """
    tol = 5e-3

    t1 = table1.copy()
    t1["C_from_lambda"] = 1.0 / t1["lambda_max_Sigma_res"]
    max_err_t1 = (t1["C_from_lambda"] - t1["C_geom_hat"]).abs().max()

    t2 = table2.copy()
    t2["baseline_C_from_lambda"] = 1.0 / t2["baseline_lambda_max"]
    t2["sym_C_from_lambda"] = 1.0 / t2["symmetry_aware_lambda_max"]
    max_err_t2_baseline = (t2["baseline_C_from_lambda"] - t2["baseline_C_geom_hat"]).abs().max()
    max_err_t2_sym = (t2["sym_C_from_lambda"] - t2["symmetry_aware_C_geom_hat"]).abs().max()

    if max_err_t1 > tol:
        raise ValueError(f"Table 1 C_geom check failed: max error = {max_err_t1:.6f}")
    if max_err_t2_baseline > tol:
        raise ValueError(f"Table 2 baseline C_geom check failed: max error = {max_err_t2_baseline:.6f}")
    if max_err_t2_sym > tol:
        raise ValueError(f"Table 2 symmetry-aware C_geom check failed: max error = {max_err_t2_sym:.6f}")


def main() -> None:
    table1 = build_table1()
    table2 = build_table2()

    validate_capacity_scores(table1, table2)

    export_table(
        table1,
        stem="table1_parametric_study",
        caption=(
            "Parametric study of geometric capacity under antisymmetric noise "
            "intensity and symmetry-aware filtering strength."
        ),
        label="tab:parametric_geometric_capacity",
    )

    export_table(
        table2,
        stem="table2_network_size_scaling",
        caption="Network-size scaling diagnostic.",
        label="tab:network_size_scaling",
    )

    print("Updated tables exported successfully.")
    print(f"Output directory: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
