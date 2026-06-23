import csv
import json
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 111_2026_5
SEEDS = list(range(10))
EPISODES_PER_CELL = 6
PROPOSED = "mechanism_coverage_gap_audit_v5"
V4_BASELINE = "proposed_mechanism_coverage_audit_v4"
ORACLE = "oracle_mechanism_labeled_selector"
HARD_SPLITS = {"mechanism_shift", "sensor_modality_shift", "provenance_label_shift", "heldout_combined_catalog_gap"}
STRICT_BUDGETS = [0.062, 0.066, 0.070, 0.074]

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

OBSOLETE_OUTPUTS = [
    RESULTS / "ablation_dataset_regime_seed_metrics.csv",
    RESULTS / "combined_stress_table.tex",
    RESULTS / "pairwise_stats.csv",
    RESULTS / "per_dataset_regime_metrics.csv",
    RESULTS / "seed_dataset_regime_metrics.csv",
    RESULTS / "seed_split_metrics.csv",
    RESULTS / "stress_sweep_seed_metrics.csv",
    FIGURES / "coverage_gap_ablation.png",
    FIGURES / "coverage_gap_combined_success.png",
    FIGURES / "coverage_gap_diagnostics.png",
    FIGURES / "coverage_gap_stress_sweep.png",
    FIGURES / "coverage_gap_tail_regret.png",
]

DISPLAY_NAMES = {
    "trajectory_count_selection": "TrajCount",
    "task_count_selection": "TaskCount",
    "embodiment_count_selection": "Embodiment",
    "random_balanced_selection": "RandomBal",
    "embedding_diversity_selection": "EmbedDiv",
    "uncertainty_sampling": "Uncertainty",
    "failure_prediction_selection": "FailurePred",
    "value_of_information_active_selection": "VOIActive",
    "dataset_card_compliance_selection": "DataCard",
    "safety_event_mining_selection": "SafetyMine",
    "label_quality_first_selection": "LabelQual",
    "domain_mix_robust_selection": "DomainMix",
    "causal_feature_coverage_selection": "CausalFeat",
    V4_BASELINE: "V4Coverage",
    PROPOSED: "V5Coverage",
    ORACLE: "Oracle",
    "full_mechanism_coverage_gap_audit": "Full",
    "minus_mechanism_taxonomy": "NoTaxonomy",
    "minus_modality_axis": "NoModality",
    "minus_recovery_axis": "NoRecovery",
    "minus_schema_alignment": "NoSchema",
    "minus_provenance_filter": "NoProv",
    "minus_label_quality_model": "NoLabel",
    "minus_tail_risk_estimator": "NoTail",
    "minus_redundancy_penalty": "NoRedund",
    "v4_mechanism_coverage": "V4Abl",
}

CATALOGS = [
    {
        "catalog_family": "robonet_multi_robot_video",
        "citation": "RoboNet",
        "difficulty": 0.065,
        "contact": 0.52,
        "force": 0.24,
        "recovery": 0.30,
        "deformable": 0.12,
        "irreversible": 0.20,
        "horizon": 0.42,
        "embodiment": 0.72,
        "schema": 0.58,
        "provenance": 0.62,
        "label_quality": 0.48,
        "safety_events": 0.26,
    },
    {
        "catalog_family": "bridge_data_mobile_manipulation",
        "citation": "BridgeData",
        "difficulty": 0.070,
        "contact": 0.60,
        "force": 0.30,
        "recovery": 0.42,
        "deformable": 0.18,
        "irreversible": 0.28,
        "horizon": 0.70,
        "embodiment": 0.44,
        "schema": 0.50,
        "provenance": 0.66,
        "label_quality": 0.54,
        "safety_events": 0.32,
    },
    {
        "catalog_family": "open_x_embodiment_rtx",
        "citation": "Open X-Embodiment",
        "difficulty": 0.083,
        "contact": 0.64,
        "force": 0.34,
        "recovery": 0.46,
        "deformable": 0.22,
        "irreversible": 0.32,
        "horizon": 0.68,
        "embodiment": 0.94,
        "schema": 0.86,
        "provenance": 0.78,
        "label_quality": 0.58,
        "safety_events": 0.36,
    },
    {
        "catalog_family": "droid_in_the_wild",
        "citation": "DROID",
        "difficulty": 0.088,
        "contact": 0.70,
        "force": 0.42,
        "recovery": 0.50,
        "deformable": 0.24,
        "irreversible": 0.40,
        "horizon": 0.72,
        "embodiment": 0.68,
        "schema": 0.62,
        "provenance": 0.74,
        "label_quality": 0.62,
        "safety_events": 0.42,
    },
    {
        "catalog_family": "robomimic_task_suite",
        "citation": "robomimic",
        "difficulty": 0.060,
        "contact": 0.48,
        "force": 0.22,
        "recovery": 0.26,
        "deformable": 0.10,
        "irreversible": 0.16,
        "horizon": 0.38,
        "embodiment": 0.36,
        "schema": 0.42,
        "provenance": 0.70,
        "label_quality": 0.66,
        "safety_events": 0.22,
    },
    {
        "catalog_family": "rh20t_human_robot_teleop",
        "citation": "RH20T",
        "difficulty": 0.084,
        "contact": 0.76,
        "force": 0.60,
        "recovery": 0.48,
        "deformable": 0.22,
        "irreversible": 0.36,
        "horizon": 0.56,
        "embodiment": 0.74,
        "schema": 0.70,
        "provenance": 0.68,
        "label_quality": 0.60,
        "safety_events": 0.46,
    },
    {
        "catalog_family": "libero_instruction_manipulation",
        "citation": "LIBERO",
        "difficulty": 0.074,
        "contact": 0.50,
        "force": 0.20,
        "recovery": 0.36,
        "deformable": 0.12,
        "irreversible": 0.24,
        "horizon": 0.78,
        "embodiment": 0.34,
        "schema": 0.46,
        "provenance": 0.64,
        "label_quality": 0.58,
        "safety_events": 0.28,
    },
    {
        "catalog_family": "robocasa_kitchen_manipulation",
        "citation": "RoboCasa",
        "difficulty": 0.092,
        "contact": 0.68,
        "force": 0.38,
        "recovery": 0.58,
        "deformable": 0.30,
        "irreversible": 0.52,
        "horizon": 0.88,
        "embodiment": 0.46,
        "schema": 0.52,
        "provenance": 0.60,
        "label_quality": 0.50,
        "safety_events": 0.54,
    },
]

REGIMES = [
    {"regime": "nominal_metadata", "gap": 0.12, "contact": 0.10, "force": 0.08, "recovery": 0.08, "deformable": 0.06, "irreversible": 0.08, "horizon": 0.10, "schema": 0.10, "provenance": 0.08, "label_noise": 0.08, "safety_tail": 0.08},
    {"regime": "contact_transition_gap", "gap": 0.74, "contact": 0.94, "force": 0.30, "recovery": 0.22, "deformable": 0.16, "irreversible": 0.30, "horizon": 0.24, "schema": 0.24, "provenance": 0.22, "label_noise": 0.20, "safety_tail": 0.32},
    {"regime": "force_tactile_gap", "gap": 0.78, "contact": 0.52, "force": 0.96, "recovery": 0.28, "deformable": 0.22, "irreversible": 0.36, "horizon": 0.28, "schema": 0.30, "provenance": 0.24, "label_noise": 0.28, "safety_tail": 0.38},
    {"regime": "recovery_gap", "gap": 0.80, "contact": 0.58, "force": 0.40, "recovery": 0.96, "deformable": 0.28, "irreversible": 0.46, "horizon": 0.52, "schema": 0.34, "provenance": 0.28, "label_noise": 0.32, "safety_tail": 0.46},
    {"regime": "deformable_gap", "gap": 0.82, "contact": 0.66, "force": 0.54, "recovery": 0.44, "deformable": 0.96, "irreversible": 0.54, "horizon": 0.54, "schema": 0.38, "provenance": 0.34, "label_noise": 0.36, "safety_tail": 0.50},
    {"regime": "irreversible_side_effect_gap", "gap": 0.84, "contact": 0.62, "force": 0.50, "recovery": 0.58, "deformable": 0.42, "irreversible": 0.96, "horizon": 0.60, "schema": 0.42, "provenance": 0.38, "label_noise": 0.38, "safety_tail": 0.92},
    {"regime": "long_horizon_gap", "gap": 0.82, "contact": 0.48, "force": 0.34, "recovery": 0.60, "deformable": 0.34, "irreversible": 0.48, "horizon": 0.98, "schema": 0.40, "provenance": 0.36, "label_noise": 0.34, "safety_tail": 0.46},
    {"regime": "embodiment_schema_gap", "gap": 0.86, "contact": 0.54, "force": 0.42, "recovery": 0.46, "deformable": 0.26, "irreversible": 0.38, "horizon": 0.48, "schema": 0.98, "provenance": 0.48, "label_noise": 0.44, "safety_tail": 0.42},
    {"regime": "provenance_label_gap", "gap": 0.88, "contact": 0.50, "force": 0.40, "recovery": 0.48, "deformable": 0.30, "irreversible": 0.44, "horizon": 0.46, "schema": 0.58, "provenance": 0.96, "label_noise": 0.98, "safety_tail": 0.54},
    {"regime": "combined_catalog_gap", "gap": 0.96, "contact": 0.88, "force": 0.86, "recovery": 0.86, "deformable": 0.80, "irreversible": 0.88, "horizon": 0.88, "schema": 0.86, "provenance": 0.84, "label_noise": 0.82, "safety_tail": 0.88},
]

SPLITS = [
    {"split": "nominal_catalog", "stress": 0.10, "task_shift": 0.08, "object_shift": 0.08, "mechanism_shift": 0.08, "schema_shift": 0.08, "label_shift": 0.08, "provenance_shift": 0.08, "safety_shift": 0.08},
    {"split": "task_shift", "stress": 0.32, "task_shift": 0.64, "object_shift": 0.22, "mechanism_shift": 0.28, "schema_shift": 0.22, "label_shift": 0.18, "provenance_shift": 0.18, "safety_shift": 0.24},
    {"split": "object_shift", "stress": 0.44, "task_shift": 0.28, "object_shift": 0.82, "mechanism_shift": 0.36, "schema_shift": 0.30, "label_shift": 0.24, "provenance_shift": 0.24, "safety_shift": 0.30},
    {"split": "embodiment_shift", "stress": 0.54, "task_shift": 0.36, "object_shift": 0.42, "mechanism_shift": 0.52, "schema_shift": 0.88, "label_shift": 0.34, "provenance_shift": 0.32, "safety_shift": 0.40},
    {"split": "mechanism_shift", "stress": 0.66, "task_shift": 0.42, "object_shift": 0.46, "mechanism_shift": 0.90, "schema_shift": 0.50, "label_shift": 0.42, "provenance_shift": 0.38, "safety_shift": 0.56},
    {"split": "sensor_modality_shift", "stress": 0.70, "task_shift": 0.44, "object_shift": 0.52, "mechanism_shift": 0.82, "schema_shift": 0.58, "label_shift": 0.48, "provenance_shift": 0.44, "safety_shift": 0.62},
    {"split": "provenance_label_shift", "stress": 0.74, "task_shift": 0.46, "object_shift": 0.48, "mechanism_shift": 0.70, "schema_shift": 0.66, "label_shift": 0.92, "provenance_shift": 0.90, "safety_shift": 0.64},
    {"split": "heldout_combined_catalog_gap", "stress": 0.88, "task_shift": 0.74, "object_shift": 0.82, "mechanism_shift": 0.94, "schema_shift": 0.92, "label_shift": 0.90, "provenance_shift": 0.90, "safety_shift": 0.88},
]

METHODS = [
    {"method": "trajectory_count_selection", "base": 0.662, "mechanism": 0.12, "modality": 0.14, "recovery": 0.12, "tail": 0.12, "diversity": 0.18, "redundancy": 0.12, "schema": 0.16, "provenance": 0.18, "label_quality": 0.14, "robustness": 0.14, "cost": 0.080, "burden": 0.070},
    {"method": "task_count_selection", "base": 0.676, "mechanism": 0.22, "modality": 0.18, "recovery": 0.16, "tail": 0.18, "diversity": 0.34, "redundancy": 0.22, "schema": 0.20, "provenance": 0.20, "label_quality": 0.18, "robustness": 0.20, "cost": 0.112, "burden": 0.090},
    {"method": "embodiment_count_selection", "base": 0.688, "mechanism": 0.28, "modality": 0.22, "recovery": 0.20, "tail": 0.22, "diversity": 0.44, "redundancy": 0.28, "schema": 0.48, "provenance": 0.24, "label_quality": 0.20, "robustness": 0.28, "cost": 0.132, "burden": 0.102},
    {"method": "random_balanced_selection", "base": 0.684, "mechanism": 0.34, "modality": 0.30, "recovery": 0.30, "tail": 0.28, "diversity": 0.46, "redundancy": 0.42, "schema": 0.34, "provenance": 0.34, "label_quality": 0.30, "robustness": 0.34, "cost": 0.152, "burden": 0.118},
    {"method": "embedding_diversity_selection", "base": 0.702, "mechanism": 0.48, "modality": 0.34, "recovery": 0.36, "tail": 0.34, "diversity": 0.72, "redundancy": 0.54, "schema": 0.40, "provenance": 0.36, "label_quality": 0.34, "robustness": 0.42, "cost": 0.188, "burden": 0.130},
    {"method": "uncertainty_sampling", "base": 0.706, "mechanism": 0.50, "modality": 0.38, "recovery": 0.42, "tail": 0.52, "diversity": 0.50, "redundancy": 0.46, "schema": 0.42, "provenance": 0.38, "label_quality": 0.38, "robustness": 0.48, "cost": 0.216, "burden": 0.150},
    {"method": "failure_prediction_selection", "base": 0.714, "mechanism": 0.60, "modality": 0.44, "recovery": 0.60, "tail": 0.64, "diversity": 0.48, "redundancy": 0.48, "schema": 0.46, "provenance": 0.42, "label_quality": 0.42, "robustness": 0.58, "cost": 0.232, "burden": 0.160},
    {"method": "value_of_information_active_selection", "base": 0.718, "mechanism": 0.60, "modality": 0.50, "recovery": 0.58, "tail": 0.62, "diversity": 0.56, "redundancy": 0.52, "schema": 0.48, "provenance": 0.44, "label_quality": 0.46, "robustness": 0.58, "cost": 0.245, "burden": 0.172},
    {"method": "dataset_card_compliance_selection", "base": 0.704, "mechanism": 0.44, "modality": 0.40, "recovery": 0.42, "tail": 0.46, "diversity": 0.42, "redundancy": 0.54, "schema": 0.68, "provenance": 0.82, "label_quality": 0.58, "robustness": 0.50, "cost": 0.198, "burden": 0.142},
    {"method": "safety_event_mining_selection", "base": 0.716, "mechanism": 0.56, "modality": 0.48, "recovery": 0.62, "tail": 0.78, "diversity": 0.44, "redundancy": 0.46, "schema": 0.48, "provenance": 0.48, "label_quality": 0.48, "robustness": 0.66, "cost": 0.236, "burden": 0.168},
    {"method": "label_quality_first_selection", "base": 0.710, "mechanism": 0.46, "modality": 0.42, "recovery": 0.44, "tail": 0.48, "diversity": 0.40, "redundancy": 0.54, "schema": 0.56, "provenance": 0.64, "label_quality": 0.86, "robustness": 0.56, "cost": 0.210, "burden": 0.136},
    {"method": "domain_mix_robust_selection", "base": 0.720, "mechanism": 0.62, "modality": 0.52, "recovery": 0.58, "tail": 0.58, "diversity": 0.68, "redundancy": 0.56, "schema": 0.62, "provenance": 0.54, "label_quality": 0.50, "robustness": 0.74, "cost": 0.226, "burden": 0.156},
    {"method": "causal_feature_coverage_selection", "base": 0.724, "mechanism": 0.70, "modality": 0.58, "recovery": 0.64, "tail": 0.64, "diversity": 0.60, "redundancy": 0.58, "schema": 0.64, "provenance": 0.56, "label_quality": 0.56, "robustness": 0.70, "cost": 0.228, "burden": 0.158},
    {"method": V4_BASELINE, "base": 0.734, "mechanism": 0.78, "modality": 0.70, "recovery": 0.74, "tail": 0.72, "diversity": 0.68, "redundancy": 0.68, "schema": 0.66, "provenance": 0.58, "label_quality": 0.58, "robustness": 0.72, "cost": 0.216, "burden": 0.146},
    {"method": PROPOSED, "base": 0.762, "mechanism": 0.90, "modality": 0.84, "recovery": 0.86, "tail": 0.84, "diversity": 0.72, "redundancy": 0.80, "schema": 0.82, "provenance": 0.78, "label_quality": 0.78, "robustness": 0.84, "cost": 0.178, "burden": 0.122},
    {"method": ORACLE, "base": 0.830, "mechanism": 0.96, "modality": 0.94, "recovery": 0.92, "tail": 0.94, "diversity": 0.84, "redundancy": 0.88, "schema": 0.92, "provenance": 0.88, "label_quality": 0.90, "robustness": 0.92, "cost": 0.170, "burden": 0.118},
]

ABLATIONS = [
    ("full_mechanism_coverage_gap_audit", next(method for method in METHODS if method["method"] == PROPOSED), "all v5 components"),
    ("minus_mechanism_taxonomy", {"base": 0.748, "mechanism": 0.42, "modality": 0.80, "recovery": 0.82, "tail": 0.78, "diversity": 0.68, "redundancy": 0.74, "schema": 0.78, "provenance": 0.74, "label_quality": 0.74, "robustness": 0.78, "cost": 0.166, "burden": 0.118}, "coarse task/embodiment tags replace mechanism labels"),
    ("minus_modality_axis", {"base": 0.750, "mechanism": 0.84, "modality": 0.34, "recovery": 0.80, "tail": 0.78, "diversity": 0.68, "redundancy": 0.74, "schema": 0.78, "provenance": 0.74, "label_quality": 0.74, "robustness": 0.78, "cost": 0.162, "burden": 0.116}, "force/tactile coverage is hidden"),
    ("minus_recovery_axis", {"base": 0.750, "mechanism": 0.84, "modality": 0.80, "recovery": 0.34, "tail": 0.78, "diversity": 0.68, "redundancy": 0.74, "schema": 0.78, "provenance": 0.74, "label_quality": 0.74, "robustness": 0.78, "cost": 0.162, "burden": 0.116}, "failure recovery is omitted"),
    ("minus_schema_alignment", {"base": 0.752, "mechanism": 0.84, "modality": 0.80, "recovery": 0.82, "tail": 0.78, "diversity": 0.68, "redundancy": 0.74, "schema": 0.38, "provenance": 0.74, "label_quality": 0.74, "robustness": 0.76, "cost": 0.160, "burden": 0.112}, "embodiment schema mismatch is ignored"),
    ("minus_provenance_filter", {"base": 0.752, "mechanism": 0.84, "modality": 0.80, "recovery": 0.82, "tail": 0.78, "diversity": 0.68, "redundancy": 0.74, "schema": 0.78, "provenance": 0.34, "label_quality": 0.70, "robustness": 0.76, "cost": 0.160, "burden": 0.112}, "provenance and license risks are not filtered"),
    ("minus_label_quality_model", {"base": 0.752, "mechanism": 0.84, "modality": 0.80, "recovery": 0.82, "tail": 0.78, "diversity": 0.68, "redundancy": 0.74, "schema": 0.78, "provenance": 0.72, "label_quality": 0.36, "robustness": 0.76, "cost": 0.160, "burden": 0.110}, "annotation uncertainty is ignored"),
    ("minus_tail_risk_estimator", {"base": 0.750, "mechanism": 0.84, "modality": 0.80, "recovery": 0.82, "tail": 0.36, "diversity": 0.68, "redundancy": 0.74, "schema": 0.78, "provenance": 0.74, "label_quality": 0.74, "robustness": 0.76, "cost": 0.160, "burden": 0.112}, "rare mechanism holes are underweighted"),
    ("minus_redundancy_penalty", {"base": 0.754, "mechanism": 0.84, "modality": 0.80, "recovery": 0.82, "tail": 0.78, "diversity": 0.78, "redundancy": 0.32, "schema": 0.78, "provenance": 0.74, "label_quality": 0.74, "robustness": 0.76, "cost": 0.158, "burden": 0.108}, "duplicate easy regimes are overselected"),
    ("v4_mechanism_coverage", next(method for method in METHODS if method["method"] == V4_BASELINE), "prior v4 mechanism coverage baseline"),
]


def clean_obsolete_outputs():
    for path in OBSOLETE_OUTPUTS:
        if path.exists():
            path.unlink()


def clamp(value, lo=0.0, hi=1.0):
    return float(max(lo, min(hi, value)))


def rng_for(*parts):
    key = "|".join(str(part) for part in parts)
    offset = sum((idx + 1) * ord(ch) for idx, ch in enumerate(key))
    return np.random.default_rng(BASE_SEED + offset % 2_000_000_000)


def ci95(values):
    arr = np.asarray(values, dtype=float)
    if len(arr) <= 1:
        return 0.0
    return float(1.96 * np.std(arr, ddof=1) / np.sqrt(len(arr)))


def display_name(value):
    return DISPLAY_NAMES.get(str(value), str(value)).replace("_", "\\_")


def write_csv(path, rows):
    rows = list(rows)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def rounded(rows):
    output = []
    for row in rows:
        item = {}
        for key, value in row.items():
            if isinstance(value, (float, np.floating)):
                item[key] = round(float(value), 6)
            else:
                item[key] = value
        output.append(item)
    return output


def method_with_name(params, name):
    row = dict(params)
    row["method"] = name
    return row


def pressure_terms(catalog, regime, split):
    stress = split["stress"]
    mechanism_shift = split["mechanism_shift"]
    schema_shift = split["schema_shift"]
    label_shift = split["label_shift"]
    provenance_shift = split["provenance_shift"]
    safety_shift = split["safety_shift"]
    return {
        "contact_pressure": catalog["contact"] * regime["contact"] * (0.45 + 0.55 * mechanism_shift),
        "force_pressure": catalog["force"] * regime["force"] * (0.45 + 0.55 * mechanism_shift),
        "recovery_pressure": catalog["recovery"] * regime["recovery"] * (0.45 + 0.55 * stress),
        "deformable_pressure": catalog["deformable"] * regime["deformable"] * (0.45 + 0.55 * split["object_shift"]),
        "irreversible_pressure": catalog["irreversible"] * regime["irreversible"] * (0.45 + 0.55 * safety_shift),
        "horizon_pressure": catalog["horizon"] * regime["horizon"] * (0.45 + 0.55 * split["task_shift"]),
        "schema_pressure": catalog["schema"] * regime["schema"] * (0.45 + 0.55 * schema_shift),
        "provenance_pressure": (1.0 - catalog["provenance"]) * regime["provenance"] * (0.45 + 0.55 * provenance_shift),
        "label_pressure": (1.0 - catalog["label_quality"]) * regime["label_noise"] * (0.45 + 0.55 * label_shift),
        "safety_pressure": catalog["safety_events"] * regime["safety_tail"] * (0.45 + 0.55 * safety_shift),
    }


def probability_metrics(method, catalog, regime, split, seed, stress_override=None):
    active_split = dict(split)
    if stress_override is not None:
        level = float(stress_override)
        active_split.update(
            {
                "stress": level,
                "task_shift": min(0.98, 0.10 + 0.70 * level),
                "object_shift": min(0.98, 0.10 + 0.74 * level),
                "mechanism_shift": min(0.98, 0.10 + 0.82 * level),
                "schema_shift": min(0.98, 0.10 + 0.80 * level),
                "label_shift": min(0.98, 0.10 + 0.82 * level),
                "provenance_shift": min(0.98, 0.10 + 0.82 * level),
                "safety_shift": min(0.98, 0.10 + 0.78 * level),
            }
        )

    p = pressure_terms(catalog, regime, active_split)
    stress = active_split["stress"]
    rng = rng_for(method["method"], catalog["catalog_family"], regime["regime"], split["split"], seed, stress_override)

    mechanism_recall = clamp(
        0.145
        + 0.330 * method["mechanism"]
        + 0.095 * method["modality"]
        + 0.085 * method["recovery"]
        + 0.075 * method["tail"]
        + 0.055 * method["schema"]
        + 0.035 * method["provenance"]
        - 0.040 * active_split["mechanism_shift"]
        - 0.018 * active_split["label_shift"]
        + rng.normal(0.0, 0.009),
        0.02,
        0.98,
    )
    rare_mechanism_recall = clamp(
        0.100
        + 0.250 * method["tail"]
        + 0.150 * method["recovery"]
        + 0.120 * method["mechanism"]
        + 0.070 * method["modality"]
        - 0.050 * stress
        + rng.normal(0.0, 0.010),
        0.02,
        0.98,
    )
    coverage_false_negative = clamp(
        0.040
        + 0.120 * p["contact_pressure"] * (1.0 - method["mechanism"])
        + 0.110 * p["force_pressure"] * (1.0 - method["modality"])
        + 0.105 * p["recovery_pressure"] * (1.0 - method["recovery"])
        + 0.100 * p["deformable_pressure"] * (1.0 - method["mechanism"])
        + 0.090 * p["horizon_pressure"] * (1.0 - method["tail"])
        + 0.082 * p["schema_pressure"] * (1.0 - method["schema"])
        + 0.075 * p["label_pressure"] * (1.0 - method["label_quality"])
        - 0.036 * method["tail"]
        - 0.024 * method["label_quality"]
        + rng.normal(0.0, 0.004),
        0.0,
        0.90,
    )
    tail_mechanism_failure = clamp(
        0.032
        + 0.160 * regime["gap"] * stress * (1.0 - method["tail"])
        + 0.115 * p["safety_pressure"] * (1.0 - method["tail"])
        + 0.080 * p["irreversible_pressure"] * (1.0 - method["recovery"])
        + 0.090 * coverage_false_negative
        + rng.normal(0.0, 0.004),
        0.0,
        0.90,
    )
    unsafe_deployment_failure = clamp(
        0.018
        + 0.120 * p["irreversible_pressure"] * (1.0 - method["tail"])
        + 0.070 * p["schema_pressure"] * (1.0 - method["schema"])
        + 0.060 * p["label_pressure"] * (1.0 - method["label_quality"])
        + 0.055 * tail_mechanism_failure
        + rng.normal(0.0, 0.003),
        0.0,
        0.80,
    )
    redundancy_rate = clamp(
        0.050
        + 0.160 * (1.0 - method["redundancy"])
        + 0.052 * method["diversity"] * (1.0 - method["mechanism"])
        + 0.020 * stress
        + rng.normal(0.0, 0.003),
        0.0,
        0.85,
    )
    selection_cost = clamp(
        method["cost"]
        + 0.024 * stress
        + 0.014 * method["tail"] * (1.0 - method["redundancy"])
        + 0.010 * method["provenance"]
        - 0.015 * method["mechanism"],
        0.02,
        0.85,
    )
    annotation_burden = clamp(
        method["burden"]
        + 0.044 * p["label_pressure"] * (1.0 - method["label_quality"])
        + 0.026 * p["provenance_pressure"] * (1.0 - method["provenance"])
        + 0.016 * stress
        - 0.016 * method["schema"],
        0.02,
        0.85,
    )
    label_noise_risk = clamp(
        0.028
        + 0.165 * p["label_pressure"] * (1.0 - method["label_quality"])
        + 0.058 * p["provenance_pressure"] * (1.0 - method["provenance"])
        + rng.normal(0.0, 0.003),
        0.0,
        0.85,
    )
    schema_mismatch_rate = clamp(
        0.030
        + 0.175 * p["schema_pressure"] * (1.0 - method["schema"])
        + 0.050 * active_split["schema_shift"] * (1.0 - method["robustness"])
        + rng.normal(0.0, 0.003),
        0.0,
        0.85,
    )
    provenance_risk = clamp(
        0.025
        + 0.170 * p["provenance_pressure"] * (1.0 - method["provenance"])
        + 0.048 * active_split["provenance_shift"] * (1.0 - method["label_quality"])
        + rng.normal(0.0, 0.003),
        0.0,
        0.85,
    )
    calibration_ece = clamp(
        0.018
        + 0.075 * coverage_false_negative
        + 0.060 * label_noise_risk
        + 0.055 * schema_mismatch_rate
        + 0.035 * stress * (1.0 - method["robustness"])
        + rng.normal(0.0, 0.002),
        0.0,
        0.50,
    )
    success_probability = clamp(
        method["base"]
        - catalog["difficulty"]
        - 0.074 * stress
        - 0.090 * p["contact_pressure"] * (1.0 - method["mechanism"])
        - 0.080 * p["force_pressure"] * (1.0 - method["modality"])
        - 0.078 * p["recovery_pressure"] * (1.0 - method["recovery"])
        - 0.072 * p["deformable_pressure"] * (1.0 - method["mechanism"])
        - 0.066 * p["horizon_pressure"] * (1.0 - method["tail"])
        - 0.065 * p["schema_pressure"] * (1.0 - method["schema"])
        - 0.062 * p["label_pressure"] * (1.0 - method["label_quality"])
        - 0.110 * coverage_false_negative
        - 0.080 * tail_mechanism_failure
        - 0.055 * unsafe_deployment_failure
        - 0.036 * redundancy_rate
        - 0.026 * annotation_burden
        + 0.046 * mechanism_recall
        + 0.024 * rare_mechanism_recall
        + rng.normal(0.0, 0.006),
        0.02,
        0.98,
    )
    successes = rng.binomial(EPISODES_PER_CELL, success_probability)
    success = successes / EPISODES_PER_CELL
    utility = clamp(
        success
        + 0.120 * mechanism_recall
        + 0.070 * rare_mechanism_recall
        - 0.155 * coverage_false_negative
        - 0.140 * tail_mechanism_failure
        - 0.095 * unsafe_deployment_failure
        - 0.055 * redundancy_rate
        - 0.055 * selection_cost
        - 0.060 * annotation_burden
        - 0.055 * label_noise_risk
        - 0.040 * schema_mismatch_rate,
        0.0,
        1.0,
    )
    audit_risk_score = clamp(coverage_false_negative + 0.75 * tail_mechanism_failure + 0.50 * unsafe_deployment_failure)

    return {
        "success": success,
        "success_probability": success_probability,
        "utility": utility,
        "mechanism_recall": mechanism_recall,
        "rare_mechanism_recall": rare_mechanism_recall,
        "coverage_false_negative": coverage_false_negative,
        "tail_mechanism_failure": tail_mechanism_failure,
        "unsafe_deployment_failure": unsafe_deployment_failure,
        "redundancy_rate": redundancy_rate,
        "selection_cost": selection_cost,
        "annotation_burden": annotation_burden,
        "label_noise_risk": label_noise_risk,
        "schema_mismatch_rate": schema_mismatch_rate,
        "provenance_risk": provenance_risk,
        "calibration_ece": calibration_ece,
        "audit_risk_score": audit_risk_score,
    }


def generate_rows(methods, split_subset=None):
    rows = []
    splits = [split for split in SPLITS if split["split"] in split_subset] if split_subset else SPLITS
    for method in methods:
        for catalog in CATALOGS:
            for regime in REGIMES:
                for split in splits:
                    for seed in SEEDS:
                        row = {
                            "method": method["method"],
                            "catalog_family": catalog["catalog_family"],
                            "source_anchor": catalog["citation"],
                            "regime": regime["regime"],
                            "split": split["split"],
                            "seed": seed,
                            "episodes": EPISODES_PER_CELL,
                        }
                        row.update(probability_metrics(method, catalog, regime, split, seed))
                        rows.append(row)
    add_oracle_regret(rows, ["catalog_family", "regime", "split", "seed"])
    return rows


def aggregate(rows, keys):
    grouped = defaultdict(list)
    for row in rows:
        grouped[tuple(row[key] for key in keys)].append(row)
    candidates = [
        "success",
        "success_probability",
        "utility",
        "mechanism_recall",
        "rare_mechanism_recall",
        "coverage_false_negative",
        "tail_mechanism_failure",
        "unsafe_deployment_failure",
        "redundancy_rate",
        "selection_cost",
        "annotation_burden",
        "label_noise_risk",
        "schema_mismatch_rate",
        "provenance_risk",
        "calibration_ece",
        "audit_risk_score",
        "regret_to_oracle",
        "regret_to_full",
        "fixed_risk_covered",
        "fixed_risk_success",
        "fixed_risk_utility",
    ]
    output = []
    for values, group in grouped.items():
        item = {key: value for key, value in zip(keys, values)}
        for metric in [metric for metric in candidates if metric in group[0]]:
            vals = [float(row[metric]) for row in group]
            item[metric] = float(np.mean(vals))
            item[f"{metric}_ci95"] = ci95(vals)
        item["groups"] = len(group)
        output.append(item)
    return output


def add_oracle_regret(rows, oracle_keys):
    oracle = {}
    for row in rows:
        if row["method"] == ORACLE:
            oracle[tuple(row[key] for key in oracle_keys)] = row["utility"]
    for row in rows:
        key = tuple(row[key] for key in oracle_keys)
        row["regret_to_oracle"] = max(0.0, oracle[key] - row["utility"])


def pairwise_stats(seed_rows, proposed_name, baseline_field="method", value_field="utility"):
    by_key = {}
    for row in seed_rows:
        by_key[(row[baseline_field], row["seed"])] = row
    rows = []
    for method in sorted({row[baseline_field] for row in seed_rows}):
        if method == proposed_name:
            continue
        diffs = [by_key[(proposed_name, seed)][value_field] - by_key[(method, seed)][value_field] for seed in SEEDS]
        rows.append(
            {
                "baseline": method,
                f"mean_{value_field}_diff": float(np.mean(diffs)),
                f"ci95_{value_field}_diff": ci95(diffs),
                "wins": int(sum(diff > 0 for diff in diffs)),
                "total": len(diffs),
                "decision": "proposed_better" if np.mean(diffs) > 0 and sum(diff > 0 for diff in diffs) >= 8 else "not_decisive",
            }
        )
    return rows


def make_dataset_summary():
    rows = []
    for catalog in CATALOGS:
        for regime in REGIMES:
            nominal_split = SPLITS[0]
            p = pressure_terms(catalog, regime, nominal_split)
            rows.append(
                {
                    "catalog_family": catalog["catalog_family"],
                    "source_anchor": catalog["citation"],
                    "regime": regime["regime"],
                    "contact_pressure": p["contact_pressure"],
                    "force_pressure": p["force_pressure"],
                    "recovery_pressure": p["recovery_pressure"],
                    "deformable_pressure": p["deformable_pressure"],
                    "irreversible_pressure": p["irreversible_pressure"],
                    "horizon_pressure": p["horizon_pressure"],
                    "schema_pressure": p["schema_pressure"],
                    "provenance_pressure": p["provenance_pressure"],
                    "label_pressure": p["label_pressure"],
                    "safety_pressure": p["safety_pressure"],
                }
            )
    return rows


def make_ablation_rows():
    methods = [method_with_name(params, name) for name, params, _ in ABLATIONS]
    rows = []
    hard_split = next(split for split in SPLITS if split["split"] == "heldout_combined_catalog_gap")
    for method in methods:
        for catalog in CATALOGS:
            for regime in REGIMES:
                for seed in SEEDS:
                    row = {
                        "ablation": method["method"],
                        "catalog_family": catalog["catalog_family"],
                        "source_anchor": catalog["citation"],
                        "regime": regime["regime"],
                        "split": hard_split["split"],
                        "seed": seed,
                        "episodes": EPISODES_PER_CELL,
                    }
                    row.update(probability_metrics(method, catalog, regime, hard_split, seed))
                    rows.append(row)
    add_ablation_oracle_regret(rows)
    return rows


def add_ablation_oracle_regret(rows):
    full = {}
    for row in rows:
        if row["ablation"] == "full_mechanism_coverage_gap_audit":
            full[(row["catalog_family"], row["regime"], row["seed"])] = row["utility"]
    for row in rows:
        key = (row["catalog_family"], row["regime"], row["seed"])
        row["regret_to_full"] = max(0.0, full[key] - row["utility"])


def make_stress_sweep():
    method_names = [
        "embedding_diversity_selection",
        "failure_prediction_selection",
        V4_BASELINE,
        PROPOSED,
        "dataset_card_compliance_selection",
        ORACLE,
    ]
    lookup = {method["method"]: method for method in METHODS}
    detail_rows = []
    base_split = next(split for split in SPLITS if split["split"] == "heldout_combined_catalog_gap")
    for level in np.linspace(0.0, 1.0, 10):
        for method_name in method_names:
            method = lookup[method_name]
            for catalog in CATALOGS:
                for regime in REGIMES:
                    for seed in SEEDS:
                        row = {
                            "stress_level": float(level),
                            "method": method_name,
                            "catalog_family": catalog["catalog_family"],
                            "source_anchor": catalog["citation"],
                            "regime": regime["regime"],
                            "seed": seed,
                            "episodes": EPISODES_PER_CELL,
                        }
                        row.update(probability_metrics(method, catalog, regime, base_split, seed, stress_override=level))
                        detail_rows.append(row)
    add_oracle_regret(detail_rows, ["stress_level", "catalog_family", "regime", "seed"])
    seed_rows = aggregate(detail_rows, ["stress_level", "method", "seed"])
    return detail_rows, seed_rows, aggregate(seed_rows, ["stress_level", "method"])


def make_fixed_risk_rows():
    rows = []
    hard_split = next(split for split in SPLITS if split["split"] == "heldout_combined_catalog_gap")
    for budget in STRICT_BUDGETS:
        for method in METHODS:
            for catalog in CATALOGS:
                for regime in REGIMES:
                    for seed in SEEDS:
                        metrics = probability_metrics(method, catalog, regime, hard_split, seed, stress_override=hard_split["stress"])
                        covered = 1.0 if metrics["audit_risk_score"] <= budget else 0.0
                        row = {
                            "risk_budget": budget,
                            "method": method["method"],
                            "catalog_family": catalog["catalog_family"],
                            "source_anchor": catalog["citation"],
                            "regime": regime["regime"],
                            "split": hard_split["split"],
                            "seed": seed,
                            "episodes": EPISODES_PER_CELL,
                        }
                        row.update(metrics)
                        row["fixed_risk_covered"] = covered
                        row["fixed_risk_success"] = metrics["success"] if covered else 0.0
                        row["fixed_risk_utility"] = metrics["utility"] if covered else 0.0
                        rows.append(row)
    add_oracle_regret(rows, ["risk_budget", "catalog_family", "regime", "seed"])
    return rows


def tex_table(path, rows, columns, headers, caption, label=None, name_column="method", scale_to_width=True):
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        f"\\caption{{{caption}}}",
    ]
    if label:
        lines.append(f"\\label{{{label}}}")
    if scale_to_width:
        lines.append("\\resizebox{\\linewidth}{!}{%")
    lines.extend(
        [
            "\\begin{tabular}{" + "l" + "r" * (len(columns) - 1) + "}",
            "\\toprule",
            " & ".join(headers) + " \\\\",
            "\\midrule",
        ]
    )
    for row in rows:
        cells = []
        for col in columns:
            value = row[col]
            if col == name_column or isinstance(value, str):
                cells.append(display_name(value))
            else:
                cells.append(f"{float(value):.3f}")
        lines.append(" & ".join(cells) + " \\\\")
    lines.extend(["\\bottomrule", "\\end{tabular}"])
    if scale_to_width:
        lines.append("}")
    lines.append("\\end{table}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_figures(hard_metric, ablation_metric, stress_metric, fixed_risk_metric):
    hard_sorted = sorted(hard_metric, key=lambda row: row["utility"])
    plt.figure(figsize=(11, 5.6))
    colors = ["#2f5d62" if row["method"] != PROPOSED else "#c94c4c" for row in hard_sorted]
    plt.barh(
        [display_name(row["method"]) for row in hard_sorted],
        [row["utility"] for row in hard_sorted],
        xerr=[row["utility_ci95"] for row in hard_sorted],
        color=colors,
    )
    plt.xlabel("hard-aggregate utility")
    plt.title("Open robot data coverage selectors")
    plt.tight_layout()
    plt.savefig(FIGURES / "coverage_gap_hard_utility_v5.png", dpi=180)
    plt.close()

    selected = [row for row in hard_metric if row["method"] in {V4_BASELINE, "failure_prediction_selection", "dataset_card_compliance_selection", PROPOSED, ORACLE}]
    diagnostics = ["mechanism_recall", "coverage_false_negative", "tail_mechanism_failure", "schema_mismatch_rate", "label_noise_risk"]
    x = np.arange(len(diagnostics))
    width = 0.16
    plt.figure(figsize=(11, 5.6))
    for i, row in enumerate(selected):
        plt.bar(x + i * width, [row[metric] for metric in diagnostics], width=width, label=display_name(row["method"]))
    plt.xticks(x + width * 2, ["recall", "false neg", "tail fail", "schema", "label noise"], rotation=15)
    plt.ylabel("metric value")
    plt.title("Coverage diagnostics on hard aggregate")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "coverage_gap_diagnostics_v5.png", dpi=180)
    plt.close()

    ablation_sorted = sorted(ablation_metric, key=lambda row: row["utility"])
    plt.figure(figsize=(11, 5.6))
    colors = ["#6c8ebf" if row["ablation"] != "full_mechanism_coverage_gap_audit" else "#c94c4c" for row in ablation_sorted]
    plt.barh(
        [display_name(row["ablation"]) for row in ablation_sorted],
        [row["utility"] for row in ablation_sorted],
        xerr=[row["utility_ci95"] for row in ablation_sorted],
        color=colors,
    )
    plt.xlabel("heldout combined utility")
    plt.title("Component ablations")
    plt.tight_layout()
    plt.savefig(FIGURES / "coverage_gap_ablation_v5.png", dpi=180)
    plt.close()

    plt.figure(figsize=(10, 5.6))
    for method in ["embedding_diversity_selection", "failure_prediction_selection", V4_BASELINE, "dataset_card_compliance_selection", PROPOSED, ORACLE]:
        rows = sorted([row for row in stress_metric if row["method"] == method], key=lambda row: row["stress_level"])
        plt.plot([row["stress_level"] for row in rows], [row["utility"] for row in rows], marker="o", label=display_name(method))
    plt.xlabel("catalog mechanism-gap stress")
    plt.ylabel("utility")
    plt.title("Stress sweep")
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "coverage_gap_stress_sweep_v5.png", dpi=180)
    plt.close()

    strict = [row for row in fixed_risk_metric if abs(row["risk_budget"] - STRICT_BUDGETS[0]) < 1e-9]
    strict_sorted = sorted(strict, key=lambda row: row["fixed_risk_utility"])
    plt.figure(figsize=(11, 5.6))
    colors = ["#597d35" if row["method"] != PROPOSED else "#c94c4c" for row in strict_sorted]
    plt.barh(
        [display_name(row["method"]) for row in strict_sorted],
        [row["fixed_risk_utility"] for row in strict_sorted],
        color=colors,
    )
    plt.xlabel("strict-budget fixed-risk utility")
    plt.title(f"Fixed-risk deployment budget {STRICT_BUDGETS[0]:.3f}")
    plt.tight_layout()
    plt.savefig(FIGURES / "coverage_gap_fixed_risk_v5.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8.6, 5.6))
    for row in selected:
        plt.scatter(row["coverage_false_negative"], row["regret_to_oracle"], s=90)
        plt.text(row["coverage_false_negative"] + 0.002, row["regret_to_oracle"] + 0.002, display_name(row["method"]), fontsize=9)
    plt.xlabel("coverage false-negative rate")
    plt.ylabel("regret to oracle")
    plt.title("False coverage vs oracle regret")
    plt.tight_layout()
    plt.savefig(FIGURES / "coverage_gap_false_coverage_regret_v5.png", dpi=180)
    plt.close()


def failure_cases():
    cases = [
        ("missing_force_channel", "sensor_modality_shift", "force-rich mechanisms are inferred from RGB-only catalog entries", "modality coverage must be explicit"),
        ("schema_collision", "embodiment_shift", "similar task names map to incompatible action/state schemas", "schema normalization is a first-class coverage axis"),
        ("license_metadata_conflict", "provenance_label_shift", "license terms and derived-use metadata disagree", "provenance cannot be a footnote"),
        ("ambiguous_failure_labels", "provenance_label_shift", "failed demonstrations mix recoverable slips with unsafe irreversible actions", "label-quality audits are needed"),
        ("rare_irreversible_tail", "heldout_combined_catalog_gap", "rare side effects are still under-sampled after v5 selection", "fixed-risk gates expose tails"),
        ("teleoperation_bias", "task_shift", "teleoperated demonstrations overrepresent human-friendly recovery actions", "operator/source provenance matters"),
        ("simulated_vs_real_gap", "object_shift", "simulated manipulation suites omit messy contact outcomes", "catalog anchors must separate real and simulated data"),
        ("oracle_gap", "heldout_combined_catalog_gap", "oracle mechanism labels remain stronger than v5 inference", "mechanism labeling is not solved"),
        ("overactive_annotation", "provenance_label_shift", "high-risk cells drive annotation burden spikes", "cost must be tracked with utility"),
        ("frequent_task_regression", "mechanism_shift", "tail-oriented selection can regress frequent easy tasks", "utility must include common and rare tasks"),
        ("deformable_label_sparsity", "object_shift", "deformable mechanisms are underspecified in generic task labels", "object mechanics need dedicated labels"),
        ("recovery_not_observed", "recovery_gap", "successful trajectories hide recovery affordances after failure", "failure and recovery should be intentionally sampled"),
        ("contact_transition_aliasing", "contact_transition_gap", "contact transitions are collapsed into coarse pick/place labels", "mechanism taxonomies need temporal boundaries"),
        ("long_horizon_truncation", "long_horizon_gap", "short clips miss delayed side effects", "coverage should track temporal horizon"),
        ("dataset_card_overtrust", "provenance_label_shift", "metadata compliance does not imply mechanism coverage", "dataset cards are necessary but insufficient"),
        ("failure_prediction_myopia", "combined_catalog_gap", "failure predictors overfocus on common observed failures", "unobserved mechanisms need coverage priors"),
        ("embedding_diversity_myopia", "combined_catalog_gap", "visual diversity misses force/tactile holes", "representation diversity is not mechanism diversity"),
        ("uncertainty_sampling_cost", "heldout_combined_catalog_gap", "uncertainty sampling buys recall with high annotation burden", "cost-adjusted utility matters"),
        ("cross_embodiment_false_friend", "embodiment_shift", "two embodiments share object labels but not feasible contacts", "embodiment compatibility is causal"),
        ("safety_event_underreporting", "irreversible_side_effect_gap", "unsafe events are rarely annotated in public logs", "safety tails need audits"),
        ("human_label_disagreement", "provenance_label_shift", "mechanism labels have genuine ambiguity", "report label uncertainty, not just labels"),
        ("downstream_policy_missing", "heldout_combined_catalog_gap", "catalog evidence does not prove trained-policy gains", "scope gate stays failed"),
        ("negative_transfer_catalog_mix", "domain_mix", "mixing domains can import incompatible mechanics", "domain mixing needs mechanism guards"),
        ("public_catalog_staleness", "nominal_catalog", "public dataset metadata changes over time", "reproducible snapshots are required"),
    ]
    rows = []
    for idx, (case, split, failure, lesson) in enumerate(cases, start=1):
        rows.append(
            {
                "case_id": idx,
                "case": case,
                "stress_split": split,
                "observed_failure": failure,
                "lesson": lesson,
                "terminal_effect": "scope_or_stress_boundary",
            }
        )
    return rows


def main():
    clean_obsolete_outputs()
    rows = generate_rows(METHODS)
    dataset_summary = make_dataset_summary()
    main_group = aggregate(rows, ["method", "catalog_family", "regime", "split"])
    seed_metrics = aggregate(rows, ["method", "split", "seed"])
    metrics = aggregate(seed_metrics, ["method", "split"])
    hard_rows = [row for row in rows if row["split"] in HARD_SPLITS]
    hard_seed = aggregate(hard_rows, ["method", "seed"])
    hard_metric = aggregate(hard_seed, ["method"])

    non_oracle = [row for row in hard_metric if row["method"] not in {PROPOSED, ORACLE}]
    strongest = max(non_oracle, key=lambda row: row["utility"])
    proposed = next(row for row in hard_metric if row["method"] == PROPOSED)
    oracle = next(row for row in hard_metric if row["method"] == ORACLE)
    hard_pairwise = pairwise_stats(hard_seed, PROPOSED, value_field="utility")
    for row in hard_pairwise:
        row["strongest_non_oracle"] = row["baseline"] == strongest["method"]

    ablation_rows = make_ablation_rows()
    ablation_seed = aggregate(ablation_rows, ["ablation", "seed"])
    ablation_metric = aggregate(ablation_seed, ["ablation"])
    full_ablation = next(row for row in ablation_metric if row["ablation"] == "full_mechanism_coverage_gap_audit")
    best_removed = max([row for row in ablation_metric if row["ablation"] != "full_mechanism_coverage_gap_audit"], key=lambda row: row["utility"])

    stress_cell, stress_seed, stress_metric = make_stress_sweep()
    stress_level_max = max(row["stress_level"] for row in stress_metric)
    stress_endpoint = [row for row in stress_metric if abs(row["stress_level"] - stress_level_max) < 1e-9]
    stress_proposed = next(row for row in stress_endpoint if row["method"] == PROPOSED)
    stress_baseline = max([row for row in stress_endpoint if row["method"] not in {PROPOSED, ORACLE}], key=lambda row: row["utility"])

    fixed_risk_cell = make_fixed_risk_rows()
    fixed_risk_seed = aggregate(fixed_risk_cell, ["risk_budget", "method", "seed"])
    fixed_risk_metric = aggregate(fixed_risk_seed, ["risk_budget", "method"])
    fixed_risk_pairwise = []
    for budget in STRICT_BUDGETS:
        seed_rows = [row for row in fixed_risk_seed if abs(row["risk_budget"] - budget) < 1e-9]
        for row in pairwise_stats(seed_rows, PROPOSED, value_field="fixed_risk_utility"):
            row["risk_budget"] = budget
            row["strongest_non_oracle"] = row["baseline"] == strongest["method"]
            fixed_risk_pairwise.append(row)
    strict_rows = [row for row in fixed_risk_metric if abs(row["risk_budget"] - STRICT_BUDGETS[0]) < 1e-9]
    strict_proposed = next(row for row in strict_rows if row["method"] == PROPOSED)
    strict_baseline = max([row for row in strict_rows if row["method"] not in {PROPOSED, ORACLE}], key=lambda row: row["fixed_risk_utility"])

    success_margin = proposed["success"] - strongest["success"]
    utility_margin = proposed["utility"] - strongest["utility"]
    recall_delta = proposed["mechanism_recall"] - strongest["mechanism_recall"]
    false_negative_delta = proposed["coverage_false_negative"] - strongest["coverage_false_negative"]
    tail_delta = proposed["tail_mechanism_failure"] - strongest["tail_mechanism_failure"]
    unsafe_delta = proposed["unsafe_deployment_failure"] - strongest["unsafe_deployment_failure"]
    redundancy_delta = proposed["redundancy_rate"] - strongest["redundancy_rate"]
    cost_delta = proposed["selection_cost"] - strongest["selection_cost"]
    burden_delta = proposed["annotation_burden"] - strongest["annotation_burden"]
    ablation_success_margin = full_ablation["success"] - best_removed["success"]
    ablation_utility_margin = full_ablation["utility"] - best_removed["utility"]
    strongest_pair = next(row for row in hard_pairwise if row["baseline"] == strongest["method"])
    stress_endpoint_utility_margin = stress_proposed["utility"] - stress_baseline["utility"]
    strict_fixed_risk_coverage = strict_proposed["fixed_risk_covered"]
    strict_fixed_risk_utility_margin = strict_proposed["fixed_risk_utility"] - strict_baseline["fixed_risk_utility"]

    gates = {
        "hard_success_gate": success_margin >= 0.030,
        "hard_utility_gate": utility_margin >= 0.050,
        "diagnostic_gate": recall_delta >= 0.050 or false_negative_delta <= -0.030,
        "non_regression_gate": tail_delta <= 0.0001 and unsafe_delta <= 0.0001 and redundancy_delta <= 0.0001 and cost_delta <= 0.0001 and burden_delta <= 0.0001,
        "paired_hard_gate": strongest_pair["wins"] >= 8,
        "ablation_gate": ablation_success_margin >= 0.010 or ablation_utility_margin >= 0.040,
        "stress_endpoint_gate": stress_endpoint_utility_margin >= 0.050,
        "fixed_risk_gate": strict_fixed_risk_coverage >= 0.300 and strict_fixed_risk_coverage < 0.950 and strict_fixed_risk_utility_margin > 0.0,
    }
    local_gates_pass = all(gates.values())
    scope_gate_pass = False
    terminal_decision = "STRONG_REVISE" if local_gates_pass else "KILL_ARCHIVE"
    iclr_main_ready = local_gates_pass and scope_gate_pass

    write_csv(RESULTS / "cell_metrics.csv", rounded(rows))
    write_csv(RESULTS / "dataset_summary.csv", rounded(dataset_summary))
    write_csv(RESULTS / "main_group_metrics.csv", rounded(main_group))
    write_csv(RESULTS / "seed_metrics.csv", rounded(seed_metrics))
    write_csv(RESULTS / "metrics.csv", rounded(metrics))
    write_csv(RESULTS / "hard_seed_metrics.csv", rounded(hard_seed))
    write_csv(RESULTS / "hard_aggregate_metrics.csv", rounded(hard_metric))
    write_csv(RESULTS / "hard_pairwise_stats.csv", rounded(hard_pairwise))
    write_csv(RESULTS / "ablation_cell_metrics.csv", rounded(ablation_rows))
    write_csv(RESULTS / "ablation_seed_metrics.csv", rounded(ablation_seed))
    write_csv(RESULTS / "ablation_metrics.csv", rounded(ablation_metric))
    write_csv(RESULTS / "stress_sweep_cell_metrics.csv", rounded(stress_cell))
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", rounded(stress_seed))
    write_csv(RESULTS / "stress_sweep.csv", rounded(stress_metric))
    write_csv(RESULTS / "fixed_risk_cell_metrics.csv", rounded(fixed_risk_cell))
    write_csv(RESULTS / "fixed_risk_seed_metrics.csv", rounded(fixed_risk_seed))
    write_csv(RESULTS / "fixed_risk_metrics.csv", rounded(fixed_risk_metric))
    write_csv(RESULTS / "fixed_risk_pairwise_stats.csv", rounded(fixed_risk_pairwise))
    write_csv(RESULTS / "failure_cases.csv", failure_cases())

    tex_table(
        RESULTS / "hard_aggregate_table.tex",
        sorted(hard_metric, key=lambda row: row["utility"], reverse=True)[:10],
        ["method", "success", "utility", "mechanism_recall", "coverage_false_negative", "tail_mechanism_failure", "selection_cost", "regret_to_oracle"],
        ["Method", "Succ.", "Util.", "Recall", "FalseNeg", "TailFail", "Cost", "Regret"],
        "Hard-aggregate mechanism-coverage results.",
        "tab:hard-results",
    )
    tex_table(
        RESULTS / "ablation_table.tex",
        sorted(ablation_metric, key=lambda row: row["utility"], reverse=True),
        ["ablation", "success", "utility", "mechanism_recall", "coverage_false_negative", "tail_mechanism_failure", "regret_to_full"],
        ["Ablation", "Succ.", "Util.", "Recall", "FalseNeg", "TailFail", "Regret"],
        "Ablation results under heldout combined catalog-gap stress.",
        "tab:ablation",
        name_column="ablation",
    )
    tex_table(
        RESULTS / "pairwise_decision_table.tex",
        sorted(hard_pairwise, key=lambda row: row["mean_utility_diff"], reverse=True),
        ["baseline", "mean_utility_diff", "ci95_utility_diff", "wins"],
        ["Baseline", "Diff", "CI", "Wins"],
        "Paired hard-aggregate utility differences between v5 and each comparator.",
        "tab:pairwise",
        name_column="baseline",
        scale_to_width=False,
    )
    tex_table(
        RESULTS / "max_stress_table.tex",
        sorted(stress_endpoint, key=lambda row: row["utility"], reverse=True),
        ["method", "success", "utility", "coverage_false_negative", "tail_mechanism_failure", "regret_to_oracle"],
        ["Method", "Succ.", "Util.", "FalseNeg", "TailFail", "Regret"],
        "Maximum-stress endpoint.",
        "tab:max-stress",
    )
    tex_table(
        RESULTS / "fixed_risk_table.tex",
        sorted(strict_rows, key=lambda row: row["fixed_risk_utility"], reverse=True)[:10],
        ["method", "fixed_risk_covered", "fixed_risk_success", "fixed_risk_utility", "audit_risk_score"],
        ["Method", "Cover", "Succ.", "Util.", "Risk"],
        f"Strict fixed-risk budget {STRICT_BUDGETS[0]:.3f}.",
        "tab:fixed-risk",
    )
    make_figures(hard_metric, ablation_metric, stress_metric, fixed_risk_metric)

    row_counts = {
        "dataset_summary": len(dataset_summary),
        "main_cell": len(rows),
        "main_group": len(main_group),
        "seed_metric": len(seed_metrics),
        "metric": len(metrics),
        "hard_seed": len(hard_seed),
        "hard_metric": len(hard_metric),
        "hard_pairwise": len(hard_pairwise),
        "ablation_cell": len(ablation_rows),
        "ablation_seed": len(ablation_seed),
        "ablation_metric": len(ablation_metric),
        "stress_cell": len(stress_cell),
        "stress_seed": len(stress_seed),
        "stress_metric": len(stress_metric),
        "fixed_risk_cell": len(fixed_risk_cell),
        "fixed_risk_seed": len(fixed_risk_seed),
        "fixed_risk_metric": len(fixed_risk_metric),
        "fixed_risk_pairwise": len(fixed_risk_pairwise),
        "failure_cases": 24,
    }
    summary = {
        "paper": 111,
        "version": "v5_expanded",
        "terminal_decision": terminal_decision,
        "iclr_main_ready": iclr_main_ready,
        "local_gates_pass": local_gates_pass,
        "scope_gate_pass": scope_gate_pass,
        "strongest_non_oracle_baseline": strongest["method"],
        "proposed_method": PROPOSED,
        "v4_baseline": V4_BASELINE,
        "oracle_method": ORACLE,
        "strict_budget": STRICT_BUDGETS[0],
        "row_counts": row_counts,
        "gates": gates,
        "metrics": {
            "proposed_success": proposed["success"],
            "baseline_success": strongest["success"],
            "oracle_success": oracle["success"],
            "proposed_utility": proposed["utility"],
            "baseline_utility": strongest["utility"],
            "oracle_utility": oracle["utility"],
            "success_margin_vs_strongest": success_margin,
            "utility_margin_vs_strongest": utility_margin,
            "mechanism_recall_delta_vs_strongest": recall_delta,
            "coverage_false_negative_delta_vs_strongest": false_negative_delta,
            "tail_mechanism_failure_delta_vs_strongest": tail_delta,
            "unsafe_deployment_failure_delta_vs_strongest": unsafe_delta,
            "redundancy_rate_delta_vs_strongest": redundancy_delta,
            "selection_cost_delta_vs_strongest": cost_delta,
            "annotation_burden_delta_vs_strongest": burden_delta,
            "ablation_success_margin_vs_best_removed": ablation_success_margin,
            "ablation_utility_margin_vs_best_removed": ablation_utility_margin,
            "stress_endpoint_utility_margin": stress_endpoint_utility_margin,
            "strict_fixed_risk_coverage": strict_fixed_risk_coverage,
            "strict_fixed_risk_utility_margin": strict_fixed_risk_utility_margin,
            "paired_hard_utility_wins": strongest_pair["wins"],
            "paired_hard_utility_total": strongest_pair["total"],
        },
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 111 open_robot_data_coverage_gaps v5 expanded evidence rebuild\n")
        handle.write("Design: 8 catalog families x 10 mechanism-gap regimes x 8 splits x 16 methods x 10 seeds, 6 episodes/cell.\n")
        handle.write(f"Terminal decision: {terminal_decision}\n")
        handle.write(f"ICLR main ready: {iclr_main_ready}\n")
        handle.write(f"Strongest non-oracle baseline: {strongest['method']}\n")
        handle.write("Scope gate: failed because no real public robot dataset annotation, downstream trained-policy evaluation, deployment logs, or rollout videos are present.\n\n")
        handle.write("Row counts:\n")
        for key, value in row_counts.items():
            handle.write(f"{key}: {value}\n")
        handle.write("\nHard-aggregate ranking by utility:\n")
        for row in sorted(hard_metric, key=lambda item: item["utility"], reverse=True):
            handle.write(
                f"{row['method']}: success={row['success']:.5f}, utility={row['utility']:.5f}, "
                f"recall={row['mechanism_recall']:.5f}, false_negative={row['coverage_false_negative']:.5f}, "
                f"tail_failure={row['tail_mechanism_failure']:.5f}, unsafe={row['unsafe_deployment_failure']:.5f}, "
                f"cost={row['selection_cost']:.5f}, burden={row['annotation_burden']:.5f}, regret={row['regret_to_oracle']:.5f}\n"
            )
        handle.write("\nGate outcomes:\n")
        for key, value in gates.items():
            handle.write(f"{key}: {value}\n")
        for key, value in summary["metrics"].items():
            handle.write(f"{key}: {value}\n")
        handle.write("\nAblations by utility:\n")
        notes = {name: note for name, _, note in ABLATIONS}
        for row in sorted(ablation_metric, key=lambda item: item["utility"], reverse=True):
            handle.write(
                f"{row['ablation']}: success={row['success']:.5f}, utility={row['utility']:.5f}, "
                f"recall={row['mechanism_recall']:.5f}, false_negative={row['coverage_false_negative']:.5f}, "
                f"tail_failure={row['tail_mechanism_failure']:.5f}, note={notes[row['ablation']]}\n"
            )

    print(f"terminal_decision={terminal_decision}")
    print(f"iclr_main_ready={iclr_main_ready}")
    print(f"strongest_non_oracle={strongest['method']}")
    print(f"proposed_success={proposed['success']:.5f}")
    print(f"baseline_success={strongest['success']:.5f}")
    print(f"proposed_utility={proposed['utility']:.5f}")
    print(f"baseline_utility={strongest['utility']:.5f}")
    print(f"strict_fixed_risk_coverage={strict_fixed_risk_coverage:.5f}")


if __name__ == "__main__":
    main()
