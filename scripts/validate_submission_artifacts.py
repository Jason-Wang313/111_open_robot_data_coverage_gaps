import csv
import hashlib
import json
import math
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
PAPER = ROOT / "paper"
DOWNLOADS_PDF = Path.home() / "Downloads" / "111.pdf"
EXPECTED_HASH = "A2204B83096B7F570DD9C429A139E71A4FA8886BA2FF99C7DC5129FFC6C8481A"
EXPECTED_ROWS = {
    "dataset_summary.csv": ("dataset_summary", 80),
    "cell_metrics.csv": ("main_cell", 102400),
    "main_group_metrics.csv": ("main_group", 10240),
    "seed_metrics.csv": ("seed_metric", 1280),
    "metrics.csv": ("metric", 128),
    "hard_seed_metrics.csv": ("hard_seed", 160),
    "hard_aggregate_metrics.csv": ("hard_metric", 16),
    "hard_pairwise_stats.csv": ("hard_pairwise", 15),
    "ablation_cell_metrics.csv": ("ablation_cell", 8000),
    "ablation_seed_metrics.csv": ("ablation_seed", 100),
    "ablation_metrics.csv": ("ablation_metric", 10),
    "stress_sweep_cell_metrics.csv": ("stress_cell", 48000),
    "stress_sweep_seed_metrics.csv": ("stress_seed", 600),
    "stress_sweep.csv": ("stress_metric", 60),
    "fixed_risk_cell_metrics.csv": ("fixed_risk_cell", 51200),
    "fixed_risk_seed_metrics.csv": ("fixed_risk_seed", 640),
    "fixed_risk_metrics.csv": ("fixed_risk_metric", 64),
    "fixed_risk_pairwise_stats.csv": ("fixed_risk_pairwise", 60),
    "failure_cases.csv": ("failure_cases", 24),
}
NUMERIC_RE = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$")


def fail(message):
    raise AssertionError(message)


def file_hash(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def pdf_pages(path):
    output = subprocess.check_output(["pdfinfo", str(path)], text=True)
    for line in output.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    fail(f"Could not read page count from {path}")


def read_csv_rows(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def check_finite_numeric(rows, path):
    for row_idx, row in enumerate(rows, start=2):
        for key, value in row.items():
            value = value.strip()
            if value and NUMERIC_RE.match(value):
                number = float(value)
                if not math.isfinite(number):
                    fail(f"Non-finite value in {path}:{row_idx} column {key}")


def check_summary():
    summary = json.loads((RESULTS / "summary.json").read_text(encoding="utf-8"))
    if summary["paper"] != 111:
        fail("summary paper id is not 111")
    if summary["version"] != "v5_expanded":
        fail("summary version is not v5_expanded")
    if summary["terminal_decision"] != "STRONG_REVISE":
        fail("terminal decision is not STRONG_REVISE")
    if summary["iclr_main_ready"] is not False:
        fail("iclr_main_ready must be false")
    if summary["local_gates_pass"] is not True:
        fail("local gates must pass")
    if summary["scope_gate_pass"] is not False:
        fail("scope gate must fail honestly")
    if not all(summary["gates"].values()):
        fail("at least one frozen local gate failed")
    metrics = summary["metrics"]
    if metrics["strict_fixed_risk_coverage"] < 0.30:
        fail("strict fixed-risk coverage below frozen lower bound")
    if metrics["strict_fixed_risk_coverage"] >= 0.95:
        fail("strict fixed-risk coverage is suspiciously perfect")
    if metrics["strict_fixed_risk_utility_margin"] <= 0:
        fail("strict fixed-risk utility margin is not positive")
    return summary


def check_rows(summary):
    for filename, (summary_key, expected_count) in EXPECTED_ROWS.items():
        path = RESULTS / filename
        if not path.exists():
            fail(f"Missing expected CSV {path}")
        rows = read_csv_rows(path)
        if len(rows) != expected_count:
            fail(f"{filename} has {len(rows)} rows, expected {expected_count}")
        if summary["row_counts"][summary_key] != expected_count:
            fail(f"summary row count {summary_key} is wrong")
        check_finite_numeric(rows, path)


def check_pdf():
    repo_pdf = PAPER / "main.pdf"
    if not repo_pdf.exists():
        fail("paper/main.pdf is missing")
    if not DOWNLOADS_PDF.exists():
        fail("Downloads/111.pdf is missing")
    if pdf_pages(repo_pdf) < 25:
        fail("paper/main.pdf is below 25 pages")
    if pdf_pages(DOWNLOADS_PDF) < 25:
        fail("Downloads/111.pdf is below 25 pages")
    repo_hash = file_hash(repo_pdf)
    downloads_hash = file_hash(DOWNLOADS_PDF)
    if repo_hash != downloads_hash:
        fail("paper/main.pdf and Downloads/111.pdf hashes differ")
    if downloads_hash != EXPECTED_HASH:
        fail(f"Unexpected Downloads/111.pdf hash {downloads_hash}")
    stray_paths = [
        Path.home() / "Desktop" / "111.pdf",
        ROOT / "111.pdf",
        ROOT.parent / "111.pdf",
    ]
    for path in stray_paths:
        if path.exists():
            fail(f"Forbidden stray numbered PDF exists: {path}")


def check_latex_and_docs():
    main_tex = (PAPER / "main.tex").read_text(encoding="utf-8")
    required_tex = [
        "colorlinks=false",
        "citebordercolor={0 0.85 0.20}",
        "linkbordercolor={1 0.55 0}",
        "urlbordercolor={0 0.45 1}",
        "pdfborder={0 0 1.5}",
        "STRONG\\_REVISE",
        "Not ICLR-main-ready",
    ]
    for token in required_tex:
        if token not in main_tex:
            fail(f"main.tex missing required token: {token}")
    for name in [
        "generated_row_counts.tex",
        "generated_gate_table.tex",
        "generated_failure_cases.tex",
        "generated_catalog_table.tex",
    ]:
        if not (PAPER / name).exists():
            fail(f"Missing generated manuscript artifact {name}")
    primary_docs = [
        ROOT / "README.md",
        ROOT / "child_status.md",
        ROOT / "docs" / "claims.md",
        ROOT / "docs" / "final_audit.md",
        ROOT / "docs" / "submission_readiness_decision.md",
        ROOT / "docs" / "submission_version_log.md",
        ROOT / "docs" / "iclr_main_gate.md",
        ROOT / "docs" / "experiment_rigor_checklist.md",
        ROOT / "docs" / "reproducibility_checklist.md",
        ROOT / "docs" / "hostile_reviewer_response.md",
        ROOT / "docs" / "submission_readiness_audit_v5.md",
        ROOT / "docs" / "paper111_terminal_audit_20260623.md",
    ]
    for path in primary_docs:
        if not path.exists():
            fail(f"Missing primary status doc {path}")
        text = path.read_text(encoding="utf-8")
        if "v5" not in text or "STRONG_REVISE" not in text:
            fail(f"Primary status doc does not describe v5 STRONG_REVISE: {path}")


def main():
    summary = check_summary()
    check_rows(summary)
    check_pdf()
    check_latex_and_docs()
    print("Paper 111 validation passed.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Paper 111 validation failed: {exc}", file=sys.stderr)
        sys.exit(1)
