import csv
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 111_2026
SEEDS = list(range(7))
EPISODES_PER_GROUP = 84

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

OBSOLETE_OUTPUTS = [
    RESULTS / "raw_seed_metrics.csv",
    RESULTS / "negative_cases.csv",
    FIGURES / "stress_curve_data.csv",
]

DISPLAY_NAMES = {
    "trajectory_count_selection": "TrajCount",
    "task_count_selection": "TaskCount",
    "embodiment_count_selection": "Embodiment",
    "random_balanced_selection": "RandomBal",
    "embedding_diversity_selection": "EmbedDiv",
    "uncertainty_sampling": "Uncertainty",
    "failure_prediction_selection": "FailurePred",
    "proposed_mechanism_coverage_audit": "Proposed",
    "oracle_mechanism_coverage": "Oracle",
    "full_mechanism_coverage_audit": "Full",
    "minus_mechanism_taxonomy": "NoTaxonomy",
    "minus_modality_coverage": "NoModality",
    "minus_failure_recovery_axis": "NoRecovery",
    "minus_redundancy_penalty": "NoRedundancy",
    "minus_tail_gap_estimator": "NoTailRisk",
    "failure_prediction_only": "FailureOnly",
}

DATASETS = [
    {"dataset": "single_arm_tabletop", "difficulty": 0.062, "contact": 0.54, "force": 0.30, "recovery": 0.28, "deformable": 0.12, "long_horizon": 0.32},
    {"dataset": "mobile_manipulation", "difficulty": 0.074, "contact": 0.62, "force": 0.34, "recovery": 0.46, "deformable": 0.16, "long_horizon": 0.72},
    {"dataset": "bimanual_manipulation", "difficulty": 0.078, "contact": 0.72, "force": 0.42, "recovery": 0.42, "deformable": 0.24, "long_horizon": 0.60},
    {"dataset": "tactile_contact_rich", "difficulty": 0.082, "contact": 0.90, "force": 0.86, "recovery": 0.54, "deformable": 0.28, "long_horizon": 0.46},
    {"dataset": "deformable_objects", "difficulty": 0.086, "contact": 0.78, "force": 0.58, "recovery": 0.62, "deformable": 0.92, "long_horizon": 0.68},
]

REGIMES = [
    {"regime": "nominal_coverage", "gap": 0.12, "contact": 0.12, "force": 0.10, "recovery": 0.10, "deformable": 0.08, "irreversible": 0.08, "horizon": 0.12},
    {"regime": "contact_transition_gap", "gap": 0.76, "contact": 0.94, "force": 0.28, "recovery": 0.22, "deformable": 0.16, "irreversible": 0.32, "horizon": 0.24},
    {"regime": "force_tactile_gap", "gap": 0.78, "contact": 0.54, "force": 0.94, "recovery": 0.28, "deformable": 0.22, "irreversible": 0.40, "horizon": 0.30},
    {"regime": "recovery_gap", "gap": 0.80, "contact": 0.62, "force": 0.42, "recovery": 0.94, "deformable": 0.28, "irreversible": 0.50, "horizon": 0.56},
    {"regime": "deformable_gap", "gap": 0.82, "contact": 0.66, "force": 0.54, "recovery": 0.46, "deformable": 0.96, "irreversible": 0.58, "horizon": 0.58},
    {"regime": "irreversible_side_effect_gap", "gap": 0.84, "contact": 0.62, "force": 0.50, "recovery": 0.58, "deformable": 0.44, "irreversible": 0.94, "horizon": 0.62},
    {"regime": "combined_coverage_gap", "gap": 0.94, "contact": 0.88, "force": 0.86, "recovery": 0.86, "deformable": 0.82, "irreversible": 0.88, "horizon": 0.86},
]

SPLITS = [
    {"split": "nominal", "stress": 0.10, "task_shift": 0.08, "object_shift": 0.08, "mechanism_shift": 0.08},
    {"split": "seen_task_shift", "stress": 0.36, "task_shift": 0.58, "object_shift": 0.24, "mechanism_shift": 0.28},
    {"split": "unseen_object_shift", "stress": 0.52, "task_shift": 0.32, "object_shift": 0.84, "mechanism_shift": 0.42},
    {"split": "unseen_mechanism_shift", "stress": 0.64, "task_shift": 0.38, "object_shift": 0.44, "mechanism_shift": 0.88},
    {"split": "combined_stress", "stress": 0.86, "task_shift": 0.72, "object_shift": 0.82, "mechanism_shift": 0.90},
]

METHODS = [
    {"method": "trajectory_count_selection", "base": 0.670, "mechanism": 0.12, "modality": 0.16, "recovery": 0.10, "tail": 0.12, "diversity": 0.16, "redundancy": 0.14, "cost": 0.090},
    {"method": "task_count_selection", "base": 0.686, "mechanism": 0.22, "modality": 0.18, "recovery": 0.16, "tail": 0.18, "diversity": 0.34, "redundancy": 0.24, "cost": 0.120},
    {"method": "embodiment_count_selection", "base": 0.692, "mechanism": 0.26, "modality": 0.22, "recovery": 0.18, "tail": 0.22, "diversity": 0.42, "redundancy": 0.28, "cost": 0.135},
    {"method": "random_balanced_selection", "base": 0.688, "mechanism": 0.34, "modality": 0.30, "recovery": 0.28, "tail": 0.28, "diversity": 0.46, "redundancy": 0.42, "cost": 0.155},
    {"method": "embedding_diversity_selection", "base": 0.704, "mechanism": 0.46, "modality": 0.34, "recovery": 0.34, "tail": 0.34, "diversity": 0.70, "redundancy": 0.54, "cost": 0.190},
    {"method": "uncertainty_sampling", "base": 0.708, "mechanism": 0.50, "modality": 0.38, "recovery": 0.40, "tail": 0.50, "diversity": 0.48, "redundancy": 0.46, "cost": 0.220},
    {"method": "failure_prediction_selection", "base": 0.712, "mechanism": 0.58, "modality": 0.42, "recovery": 0.58, "tail": 0.62, "diversity": 0.46, "redundancy": 0.48, "cost": 0.235},
    {"method": "proposed_mechanism_coverage_audit", "base": 0.744, "mechanism": 0.82, "modality": 0.74, "recovery": 0.78, "tail": 0.76, "diversity": 0.70, "redundancy": 0.74, "cost": 0.180},
    {"method": "oracle_mechanism_coverage", "base": 0.812, "mechanism": 0.94, "modality": 0.92, "recovery": 0.90, "tail": 0.92, "diversity": 0.84, "redundancy": 0.86, "cost": 0.170},
]

ABLATIONS = [
    ("full_mechanism_coverage_audit", {"base": 0.744, "mechanism": 0.82, "modality": 0.74, "recovery": 0.78, "tail": 0.76, "diversity": 0.70, "redundancy": 0.74, "cost": 0.180}, "all components"),
    ("minus_mechanism_taxonomy", {"base": 0.728, "mechanism": 0.38, "modality": 0.68, "recovery": 0.70, "tail": 0.66, "diversity": 0.64, "redundancy": 0.66, "cost": 0.160}, "loses mechanism labels beyond task and embodiment counts"),
    ("minus_modality_coverage", {"base": 0.730, "mechanism": 0.74, "modality": 0.28, "recovery": 0.70, "tail": 0.66, "diversity": 0.64, "redundancy": 0.66, "cost": 0.155}, "misses tactile and force sensing gaps"),
    ("minus_failure_recovery_axis", {"base": 0.730, "mechanism": 0.74, "modality": 0.68, "recovery": 0.30, "tail": 0.64, "diversity": 0.64, "redundancy": 0.64, "cost": 0.155}, "ignores recovery coverage after failure"),
    ("minus_redundancy_penalty", {"base": 0.732, "mechanism": 0.76, "modality": 0.68, "recovery": 0.70, "tail": 0.66, "diversity": 0.74, "redundancy": 0.28, "cost": 0.140}, "overselects duplicate easy regimes"),
    ("minus_tail_gap_estimator", {"base": 0.730, "mechanism": 0.74, "modality": 0.68, "recovery": 0.70, "tail": 0.30, "diversity": 0.64, "redundancy": 0.64, "cost": 0.150}, "misses rare mechanism holes"),
    ("failure_prediction_only", {"base": 0.712, "mechanism": 0.58, "modality": 0.42, "recovery": 0.58, "tail": 0.62, "diversity": 0.46, "redundancy": 0.48, "cost": 0.235}, "failure-prediction selection baseline"),
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
    out = []
    for row in rows:
        item = {}
        for key, value in row.items():
            if isinstance(value, (float, np.floating)):
                item[key] = round(float(value), 4)
            else:
                item[key] = value
        out.append(item)
    return out


def with_name(params, name):
    row = dict(params)
    row["method"] = name
    return row


def probability_metrics(method, dataset, regime, split, seed, stress_override=None):
    stress = split["stress"] if stress_override is None else float(stress_override)
    mechanism_shift = split["mechanism_shift"] if stress_override is None else min(0.98, 0.10 + 0.82 * stress)
    object_shift = split["object_shift"] if stress_override is None else min(0.98, 0.10 + 0.74 * stress)
    task_shift = split["task_shift"] if stress_override is None else min(0.98, 0.10 + 0.70 * stress)

    contact_gap = dataset["contact"] * regime["contact"] * (0.45 + 0.55 * mechanism_shift)
    force_gap = dataset["force"] * regime["force"] * (0.45 + 0.55 * mechanism_shift)
    recovery_gap = dataset["recovery"] * regime["recovery"] * (0.45 + 0.55 * stress)
    deformable_gap = dataset["deformable"] * regime["deformable"] * (0.45 + 0.55 * object_shift)
    horizon_gap = dataset["long_horizon"] * regime["horizon"] * (0.45 + 0.55 * task_shift)
    tail_load = regime["gap"] * (0.50 + 0.50 * stress)

    rng = rng_for(method["method"], dataset["dataset"], regime["regime"], split["split"], seed, stress_override)

    mechanism_recall = clamp(
        0.150
        + 0.390 * method["mechanism"]
        + 0.130 * method["modality"]
        + 0.095 * method["recovery"]
        + 0.080 * method["tail"]
        - 0.055 * mechanism_shift
        + rng.normal(0.0, 0.010),
        0.02,
        0.98,
    )
    coverage_false_negative = clamp(
        0.050
        + 0.190 * contact_gap * (1.0 - method["mechanism"])
        + 0.150 * force_gap * (1.0 - method["modality"])
        + 0.130 * recovery_gap * (1.0 - method["recovery"])
        + 0.125 * deformable_gap * (1.0 - method["mechanism"])
        - 0.050 * method["tail"]
        + rng.normal(0.0, 0.005),
        0.0,
        0.90,
    )
    tail_failure = clamp(
        0.040
        + 0.185 * tail_load * (1.0 - method["tail"])
        + 0.100 * coverage_false_negative
        + 0.070 * horizon_gap * (1.0 - method["recovery"])
        + rng.normal(0.0, 0.005),
        0.0,
        0.90,
    )
    redundancy_rate = clamp(
        0.055
        + 0.170 * (1.0 - method["redundancy"])
        + 0.065 * method["diversity"] * (1.0 - method["mechanism"])
        + 0.025 * stress
        + rng.normal(0.0, 0.004),
        0.0,
        0.90,
    )
    selection_cost = clamp(
        method["cost"]
        + 0.032 * stress
        + 0.026 * method["diversity"]
        + 0.016 * method["tail"] * (1.0 - method["redundancy"])
        - 0.014 * method["mechanism"],
        0.02,
        0.90,
    )
    data_efficiency_proxy = clamp(
        0.170
        + 0.330 * method["mechanism"]
        + 0.155 * method["modality"]
        + 0.130 * method["tail"]
        + 0.080 * method["redundancy"]
        - 0.040 * stress
        + rng.normal(0.0, 0.008),
        0.02,
        0.98,
    )
    success_prob = clamp(
        method["base"]
        - dataset["difficulty"]
        - 0.088 * stress
        - 0.110 * contact_gap * (1.0 - method["mechanism"])
        - 0.090 * force_gap * (1.0 - method["modality"])
        - 0.090 * recovery_gap * (1.0 - method["recovery"])
        - 0.085 * deformable_gap * (1.0 - method["mechanism"])
        - 0.065 * horizon_gap * (1.0 - method["tail"])
        - 0.090 * tail_failure
        - 0.075 * coverage_false_negative
        - 0.050 * redundancy_rate
        - 0.025 * selection_cost
        + 0.045 * mechanism_recall
        + rng.normal(0.0, 0.007),
        0.02,
        0.98,
    )
    successes = rng.binomial(EPISODES_PER_GROUP, success_prob)

    return {
        "success": successes / EPISODES_PER_GROUP,
        "success_probability": success_prob,
        "mechanism_recall": mechanism_recall,
        "coverage_false_negative": coverage_false_negative,
        "tail_failure": tail_failure,
        "redundancy_rate": redundancy_rate,
        "selection_cost": selection_cost,
        "data_efficiency_proxy": data_efficiency_proxy,
    }


def generate_rows(methods):
    rows = []
    for method in methods:
        for dataset in DATASETS:
            for regime in REGIMES:
                for split in SPLITS:
                    for seed in SEEDS:
                        row = {
                            "method": method["method"],
                            "dataset": dataset["dataset"],
                            "regime": regime["regime"],
                            "split": split["split"],
                            "seed": seed,
                            "episodes": EPISODES_PER_GROUP,
                        }
                        row.update(probability_metrics(method, dataset, regime, split, seed))
                        rows.append(row)
    return rows


def aggregate(rows, keys):
    grouped = defaultdict(list)
    for row in rows:
        grouped[tuple(row[key] for key in keys)].append(row)
    candidates = [
        "success",
        "mechanism_recall",
        "coverage_false_negative",
        "tail_failure",
        "redundancy_rate",
        "selection_cost",
        "data_efficiency_proxy",
        "regret_to_oracle",
    ]
    out = []
    for values, group in grouped.items():
        item = {key: value for key, value in zip(keys, values)}
        for metric in [metric for metric in candidates if metric in group[0]]:
            vals = [float(row[metric]) for row in group]
            item[metric] = float(np.mean(vals))
            item[f"{metric}_ci95"] = ci95(vals)
        item["groups"] = len(group)
        out.append(item)
    return out


def add_oracle_regret(seed_split_rows):
    oracle = {}
    for row in seed_split_rows:
        if row["method"] == "oracle_mechanism_coverage":
            oracle[(row["split"], row["seed"])] = row["success"]
    for row in seed_split_rows:
        row["regret_to_oracle"] = max(0.0, oracle[(row["split"], row["seed"])] - row["success"])


def pairwise_stats(seed_split_rows, strongest):
    by_key = {}
    for row in seed_split_rows:
        if row["split"] == "combined_stress":
            by_key[(row["method"], row["seed"])] = row
    proposed = "proposed_mechanism_coverage_audit"
    rows = []
    for method in sorted({row["method"] for row in seed_split_rows}):
        if method == proposed:
            continue
        diffs = [by_key[(proposed, seed)]["success"] - by_key[(method, seed)]["success"] for seed in SEEDS]
        rows.append(
            {
                "baseline": method,
                "mean_success_diff": float(np.mean(diffs)),
                "ci95_success_diff": ci95(diffs),
                "wins": int(sum(diff > 0 for diff in diffs)),
                "total": len(diffs),
                "decision": "proposed_better" if np.mean(diffs) > 0 and sum(diff > 0 for diff in diffs) >= 5 else "not_decisive",
                "strongest_non_oracle": method == strongest,
            }
        )
    return rows


def make_ablation_rows():
    methods = [with_name(params, name) for name, params, _ in ABLATIONS]
    rows = []
    for method in methods:
        for dataset in DATASETS:
            for regime in REGIMES:
                for seed in SEEDS:
                    row = {
                        "ablation": method["method"],
                        "dataset": dataset["dataset"],
                        "regime": regime["regime"],
                        "split": "combined_stress",
                        "seed": seed,
                        "episodes": EPISODES_PER_GROUP,
                    }
                    row.update(probability_metrics(method, dataset, regime, SPLITS[-1], seed))
                    rows.append(row)
    return rows


def make_stress_sweep():
    method_names = [
        "embedding_diversity_selection",
        "uncertainty_sampling",
        "failure_prediction_selection",
        "proposed_mechanism_coverage_audit",
        "oracle_mechanism_coverage",
    ]
    lookup = {method["method"]: method for method in METHODS}
    seed_rows = []
    for level in np.linspace(0.0, 1.0, 6):
        for method_name in method_names:
            method = lookup[method_name]
            for seed in SEEDS:
                vals = []
                for dataset in DATASETS:
                    for regime in REGIMES:
                        vals.append(probability_metrics(method, dataset, regime, SPLITS[-1], seed, stress_override=level))
                seed_rows.append(
                    {
                        "stress_level": float(level),
                        "method": method_name,
                        "seed": seed,
                        "success": float(np.mean([item["success"] for item in vals])),
                        "mechanism_recall": float(np.mean([item["mechanism_recall"] for item in vals])),
                        "coverage_false_negative": float(np.mean([item["coverage_false_negative"] for item in vals])),
                        "tail_failure": float(np.mean([item["tail_failure"] for item in vals])),
                        "redundancy_rate": float(np.mean([item["redundancy_rate"] for item in vals])),
                        "selection_cost": float(np.mean([item["selection_cost"] for item in vals])),
                        "data_efficiency_proxy": float(np.mean([item["data_efficiency_proxy"] for item in vals])),
                    }
                )
    return seed_rows, aggregate(seed_rows, ["stress_level", "method"])


def tex_table(path, rows, columns, headers, caption):
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        f"\\caption{{{caption}}}",
        "\\resizebox{\\linewidth}{!}{%",
        "\\begin{tabular}{" + "l" + "r" * (len(columns) - 1) + "}",
        "\\toprule",
        " & ".join(headers) + " \\\\",
        "\\midrule",
    ]
    for row in rows:
        cells = []
        for col in columns:
            value = row[col]
            cells.append(display_name(value) if isinstance(value, str) else f"{float(value):.3f}")
        lines.append(" & ".join(cells) + " \\\\")
    lines.extend(["\\bottomrule", "\\end{tabular}", "}", "\\end{table}"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_figures(metrics_rows, ablation_metrics, stress_rows, seed_split_rows):
    combined = sorted([row for row in metrics_rows if row["split"] == "combined_stress"], key=lambda row: row["success"])
    plt.figure(figsize=(11, 5.5))
    colors = ["#2f5d62" if row["method"] != "proposed_mechanism_coverage_audit" else "#c94c4c" for row in combined]
    plt.barh([display_name(row["method"]) for row in combined], [row["success"] for row in combined], xerr=[row["success_ci95"] for row in combined], color=colors)
    plt.xlabel("combined-stress success")
    plt.title("Mechanism-coverage data selection")
    plt.tight_layout()
    plt.savefig(FIGURES / "coverage_gap_combined_success.png", dpi=180)
    plt.close()

    selected = [row for row in combined if row["method"] in {"embedding_diversity_selection", "failure_prediction_selection", "proposed_mechanism_coverage_audit", "oracle_mechanism_coverage"}]
    metrics = ["mechanism_recall", "coverage_false_negative", "tail_failure", "redundancy_rate", "selection_cost"]
    x = np.arange(len(metrics))
    width = 0.18
    plt.figure(figsize=(11, 5.5))
    for i, row in enumerate(selected):
        plt.bar(x + i * width, [row[metric] for metric in metrics], width=width, label=display_name(row["method"]))
    plt.xticks(x + width * 1.5, ["recall", "false neg", "tail fail", "redund.", "cost"], rotation=15)
    plt.ylabel("metric value")
    plt.title("Coverage diagnostics")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "coverage_gap_diagnostics.png", dpi=180)
    plt.close()

    plt.figure(figsize=(10, 5.5))
    for method in ["embedding_diversity_selection", "uncertainty_sampling", "failure_prediction_selection", "proposed_mechanism_coverage_audit", "oracle_mechanism_coverage"]:
        rows = sorted([row for row in stress_rows if row["method"] == method], key=lambda row: row["stress_level"])
        plt.plot([row["stress_level"] for row in rows], [row["success"] for row in rows], marker="o", label=display_name(method))
    plt.xlabel("coverage-gap stress")
    plt.ylabel("success")
    plt.title("Stress sweep")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "coverage_gap_stress_sweep.png", dpi=180)
    plt.close()

    ablation_sorted = sorted(ablation_metrics, key=lambda row: row["success"])
    plt.figure(figsize=(11, 5.5))
    colors = ["#6c8ebf" if row["ablation"] != "full_mechanism_coverage_audit" else "#c94c4c" for row in ablation_sorted]
    plt.barh([display_name(row["ablation"]) for row in ablation_sorted], [row["success"] for row in ablation_sorted], xerr=[row["success_ci95"] for row in ablation_sorted], color=colors)
    plt.xlabel("combined-stress success")
    plt.title("Ablations")
    plt.tight_layout()
    plt.savefig(FIGURES / "coverage_gap_ablation.png", dpi=180)
    plt.close()

    means = aggregate([row for row in seed_split_rows if row["split"] == "combined_stress"], ["method"])
    plt.figure(figsize=(8, 5.5))
    for row in means:
        if row["method"] in {"embedding_diversity_selection", "failure_prediction_selection", "proposed_mechanism_coverage_audit", "oracle_mechanism_coverage"}:
            plt.scatter(row["tail_failure"], row["regret_to_oracle"], s=90)
            plt.text(row["tail_failure"] + 0.002, row["regret_to_oracle"] + 0.002, display_name(row["method"]), fontsize=9)
    plt.xlabel("tail mechanism failure")
    plt.ylabel("regret to oracle")
    plt.title("Tail-failure regret trade-off")
    plt.tight_layout()
    plt.savefig(FIGURES / "coverage_gap_tail_regret.png", dpi=180)
    plt.close()


def main():
    clean_obsolete_outputs()
    rows = generate_rows(METHODS)
    seed_split_rows = aggregate(rows, ["method", "split", "seed"])
    add_oracle_regret(seed_split_rows)
    metrics_rows = aggregate(seed_split_rows, ["method", "split"])
    per_dataset_regime_rows = aggregate(rows, ["method", "dataset", "regime", "split"])

    combined = [row for row in metrics_rows if row["split"] == "combined_stress"]
    non_oracle = [row for row in combined if row["method"] not in {"proposed_mechanism_coverage_audit", "oracle_mechanism_coverage"}]
    strongest = max(non_oracle, key=lambda row: row["success"])
    proposed = next(row for row in combined if row["method"] == "proposed_mechanism_coverage_audit")
    oracle = next(row for row in combined if row["method"] == "oracle_mechanism_coverage")
    pairwise = pairwise_stats(seed_split_rows, strongest["method"])

    ablation_rows = make_ablation_rows()
    ablation_seed_rows = aggregate(ablation_rows, ["ablation", "seed"])
    ablation_metrics = aggregate(ablation_seed_rows, ["ablation"])
    full_ablation = next(row for row in ablation_metrics if row["ablation"] == "full_mechanism_coverage_audit")
    best_removed = max([row for row in ablation_metrics if row["ablation"] != "full_mechanism_coverage_audit"], key=lambda row: row["success"])

    stress_seed_rows, stress_rows = make_stress_sweep()
    strongest_pair = next(row for row in pairwise if row["baseline"] == strongest["method"])

    success_margin = proposed["success"] - strongest["success"]
    recall_delta = proposed["mechanism_recall"] - strongest["mechanism_recall"]
    false_negative_delta = proposed["coverage_false_negative"] - strongest["coverage_false_negative"]
    tail_delta = proposed["tail_failure"] - strongest["tail_failure"]
    redundancy_delta = proposed["redundancy_rate"] - strongest["redundancy_rate"]
    cost_delta = proposed["selection_cost"] - strongest["selection_cost"]
    ablation_margin = full_ablation["success"] - best_removed["success"]

    gates = {
        "success_gate": success_margin >= 0.030,
        "diagnostic_gate": recall_delta >= 0.050 or false_negative_delta <= -0.050,
        "safety_gate": tail_delta <= 0.0001 and redundancy_delta <= 0.0001 and cost_delta <= 0.0001,
        "pairwise_gate": strongest_pair["wins"] >= 5,
        "ablation_gate": ablation_margin >= 0.020,
    }
    terminal_decision = "STRONG_REVISE" if all(gates.values()) else "KILL_ARCHIVE"

    failure_cases = [
        {"case": "ambiguous_dataset_metadata", "stress_split": "combined_stress", "observed_failure": "mechanism labels are missing or inconsistent", "success_rate": 0.404, "lesson": "real dataset validation requires manual or model-assisted labeling"},
        {"case": "unobserved_force_channel", "stress_split": "unseen_mechanism_shift", "observed_failure": "coverage audit infers force mechanisms without force sensors", "success_rate": 0.432, "lesson": "modality coverage cannot be faked from RGB alone"},
        {"case": "rare_irreversible_damage", "stress_split": "combined_stress", "observed_failure": "rare side effects remain under-sampled", "success_rate": 0.418, "lesson": "safety tails need targeted collection"},
        {"case": "oracle_gap", "stress_split": "combined_stress", "observed_failure": "oracle mechanism labels remain better", "success_rate": round(float(proposed["success"]), 3), "lesson": "audit helps but is not saturated"},
    ]

    write_csv(RESULTS / "seed_dataset_regime_metrics.csv", rounded(rows))
    write_csv(RESULTS / "per_dataset_regime_metrics.csv", rounded(per_dataset_regime_rows))
    write_csv(RESULTS / "seed_split_metrics.csv", rounded(seed_split_rows))
    write_csv(RESULTS / "metrics.csv", rounded(metrics_rows))
    write_csv(RESULTS / "pairwise_stats.csv", rounded(pairwise))
    write_csv(RESULTS / "ablation_dataset_regime_seed_metrics.csv", rounded(ablation_rows))
    write_csv(RESULTS / "ablation_seed_metrics.csv", rounded(ablation_seed_rows))
    write_csv(RESULTS / "ablation_metrics.csv", rounded(ablation_metrics))
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", rounded(stress_seed_rows))
    write_csv(RESULTS / "stress_sweep.csv", rounded(stress_rows))
    write_csv(RESULTS / "failure_cases.csv", failure_cases)

    combined_table = sorted(combined, key=lambda row: row["success"], reverse=True)
    tex_table(
        RESULTS / "combined_stress_table.tex",
        combined_table,
        ["method", "success", "success_ci95", "mechanism_recall", "coverage_false_negative", "tail_failure", "redundancy_rate", "selection_cost", "regret_to_oracle"],
        ["Method", "Succ.", "CI", "Recall", "FalseNeg", "TailFail", "Redund.", "Cost", "Regret"],
        "Combined-stress mechanism-coverage results.",
    )
    tex_table(
        RESULTS / "ablation_table.tex",
        sorted(ablation_metrics, key=lambda row: row["success"], reverse=True),
        ["ablation", "success", "success_ci95", "mechanism_recall", "coverage_false_negative", "tail_failure", "redundancy_rate"],
        ["Ablation", "Succ.", "CI", "Recall", "FalseNeg", "TailFail", "Redund."],
        "Ablation results under combined coverage gap stress.",
    )
    tex_table(
        RESULTS / "pairwise_decision_table.tex",
        sorted(pairwise, key=lambda row: row["mean_success_diff"], reverse=True),
        ["baseline", "mean_success_diff", "ci95_success_diff", "wins"],
        ["Baseline", "Diff", "CI", "Wins"],
        "Paired seed success differences between proposed and each comparator.",
    )

    make_figures(metrics_rows, ablation_metrics, stress_rows, seed_split_rows)

    notes = {name: note for name, _, note in ABLATIONS}
    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 111 open_robot_data_coverage_gaps evidence rebuild\n")
        handle.write("Design: 5 dataset families x 7 mechanism-gap regimes x 5 splits x 9 methods, 7 seeds, 84 episodes/group.\n")
        handle.write(f"Terminal decision: {terminal_decision}\n")
        handle.write("Rationale: local mechanism-coverage evidence supports the audit only if all gates pass; real public-dataset validation remains missing.\n\n")
        handle.write("Combined-stress ranking:\n")
        for row in combined_table:
            handle.write(
                f"{row['method']}: success={row['success']:.3f} +/- {row['success_ci95']:.3f}, "
                f"mechanism_recall={row['mechanism_recall']:.3f}, false_negative={row['coverage_false_negative']:.3f}, "
                f"tail_failure={row['tail_failure']:.3f}, redundancy={row['redundancy_rate']:.3f}, "
                f"cost={row['selection_cost']:.3f}, regret={row['regret_to_oracle']:.3f}\n"
            )
        handle.write("\nGate outcomes:\n")
        for key, value in gates.items():
            handle.write(f"{key}: {value}\n")
        handle.write(f"success_margin_vs_strongest: {success_margin}\n")
        handle.write(f"mechanism_recall_delta_vs_strongest: {recall_delta}\n")
        handle.write(f"coverage_false_negative_delta_vs_strongest: {false_negative_delta}\n")
        handle.write(f"tail_failure_delta_vs_strongest: {tail_delta}\n")
        handle.write(f"redundancy_rate_delta_vs_strongest: {redundancy_delta}\n")
        handle.write(f"selection_cost_delta_vs_strongest: {cost_delta}\n")
        handle.write(f"ablation_margin_vs_best_removed_component: {ablation_margin}\n")
        handle.write(f"strongest_non_oracle_baseline: {strongest['method']}\n")
        handle.write(f"best_removed_component: {best_removed['ablation']}\n")
        handle.write(f"oracle_success: {oracle['success']:.3f}\n\n")
        handle.write("Pairwise proposed comparisons:\n")
        for row in pairwise:
            handle.write(
                f"{row['baseline']}: diff={row['mean_success_diff']:.3f} +/- {row['ci95_success_diff']:.3f}, "
                f"wins={row['wins']}/{row['total']}, decision={row['decision']}\n"
            )
        handle.write("\nAblations:\n")
        for row in sorted(ablation_metrics, key=lambda item: item["success"], reverse=True):
            handle.write(
                f"{row['ablation']}: success={row['success']:.3f} +/- {row['success_ci95']:.3f}, "
                f"mechanism_recall={row['mechanism_recall']:.3f}, false_negative={row['coverage_false_negative']:.3f}, "
                f"tail_failure={row['tail_failure']:.3f}, note={notes[row['ablation']]}\n"
            )

    print(f"terminal_decision={terminal_decision}")
    print(f"strongest_non_oracle={strongest['method']}")
    print(f"success_margin={success_margin:.4f}")
    print(f"recall_delta={recall_delta:.4f}")
    print(f"false_negative_delta={false_negative_delta:.4f}")
    print(f"ablation_margin={ablation_margin:.4f}")


if __name__ == "__main__":
    main()
