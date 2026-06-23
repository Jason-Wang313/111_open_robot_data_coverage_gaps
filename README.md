# 111 Open Robot Data Coverage Gaps

Submission-hardening version: v5_expanded

Terminal decision: STRONG_REVISE.

ICLR main readiness: no. The v5 local/catalog audit is substantially stronger than v4.1, but the scope gate still fails because no real public-dataset annotation campaign, label-quality audit, downstream trained-policy evaluation, deployment log, or rollout-video evidence is present.

## Evidence Snapshot

- Protocol: 8 catalog-style public robot dataset anchors, 10 mechanism-gap regimes, 8 deployment splits, 16 methods, and 10 paired seeds.
- Main evidence: 102,400 main cells, 10,240 grouped cells, 1,280 seed metrics, and 128 aggregate metrics.
- Added rigor: 8,000 ablation cells, 48,000 stress cells, 51,200 fixed-risk cells, 60 fixed-risk pairwise comparisons, and 24 retained failure cases.
- Strongest non-oracle baseline: `proposed_mechanism_coverage_audit_v4`.
- Proposed method: `mechanism_coverage_gap_audit_v5`.
- Hard success: `0.65063` proposed vs `0.58526` strongest baseline.
- Hard utility: `0.72744` proposed vs `0.63780` strongest baseline.
- Mechanism recall delta: `+0.08828`.
- Coverage false-negative delta: `-0.02588`.
- Tail mechanism failure delta: `-0.01640`.
- Unsafe deployment failure delta: `-0.00682`.
- Paired hard utility wins: `10/10`.
- Strict fixed-risk coverage: `0.32000`, intentionally non-perfect.
- Strict fixed-risk utility margin: `0.16322`.

## Artifacts

- Canonical PDF: `C:/Users/wangz/Downloads/111.pdf`
- PDF pages: 25
- PDF SHA256: `A2204B83096B7F570DD9C429A139E71A4FA8886BA2FF99C7DC5129FFC6C8481A`
- Public repository: `https://github.com/Jason-Wang313/111_open_robot_data_coverage_gaps`
- Numbered PDF rule: `111.pdf` belongs in Downloads only, not on Desktop and not in repo roots.

## Reproduce

```powershell
python src\run_experiment.py
python scripts\generate_manuscript.py
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

## Validate

```powershell
python scripts\validate_submission_artifacts.py
```

The validator must pass while preserving the honest `STRONG_REVISE` decision and failed external scope gate.
