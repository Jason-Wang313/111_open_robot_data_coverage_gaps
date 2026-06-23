# Paper 111 Expanded Submission Plan

Frozen before v5 experiment/manuscript edits: 2026-06-23 12:13:00 +08:00

## Objective

Convert Paper 111 from a short v4.1 local audit into a 25+ page evidence-bound ICLR-main-target manuscript while preserving the central honesty constraint: local/catalog evidence may earn `STRONG_REVISE`, but it cannot earn ICLR-main readiness without real public-dataset annotation and downstream trained-policy validation.

## Starting Point

- Current version: v4.1.
- Current PDF: 6 pages at `C:/Users/wangz/Downloads/111.pdf`.
- Current decision: `STRONG_REVISE`.
- Current blocker: no real public robot dataset validation, no downstream trained policies, no label-quality audit.
- Current evidence scale: 5 dataset families, 7 regimes, 5 splits, 9 methods, 7 seeds, 84 held-out episodes per group.

## Planned v5 Changes

1. Replace the v4 experiment with `mechanism_coverage_gap_audit_v5`.
2. Expand the benchmark to 8 catalog-style public robot dataset families, 10 mechanism-gap regimes, 8 deployment splits, 16 methods, and 10 seeds.
3. Add hard-aggregate analysis over the hardest deployment splits.
4. Add strong baselines beyond count/diversity/failure prediction: value-of-information active selection, dataset-card compliance, safety-event mining, label-quality-first selection, domain-mix robust selection, causal-feature coverage, and v4 proposed mechanism coverage.
5. Add fixed-risk calibration under false-negative and tail-failure budgets.
6. Add stress sweeps, ablations, failure cases, and a public-catalog metadata audit table.
7. Generate a 25+ page PDF with bright boxed clickable citation links.
8. Validate artifact placement, hash, row counts, page count, link settings, and stale-documentation absence.
9. Commit and push the public GitHub repo only after validation.
10. Update shared root status files after the repo and PDF are verified.

## Frozen Local Decision Gates

`STRONG_REVISE` requires all local gates:

- Hard success margin over strongest non-oracle baseline >= 0.030.
- Hard utility margin over strongest non-oracle baseline >= 0.050.
- Mechanism recall improves >= 0.050 or coverage false negatives improve <= -0.030.
- Tail failure, unsafe deployment failure, redundancy, annotation burden, and selection cost do not increase.
- Paired hard-split utility wins >= 8/10 seeds.
- Best removed-component ablation is below full v5 by >= 0.010 success or >= 0.040 utility.
- Maximum-stress endpoint utility margin >= 0.050.
- Strict fixed-risk coverage >= 0.300 and not trivially perfect; strict fixed-risk utility margin > 0.

`KILL_ARCHIVE` if any local gate fails.

## Non-Negotiable Scope Gate

ICLR-main ready remains `no` unless real public robot datasets are audited with label-quality checks and downstream trained-policy evaluations. No local synthetic or catalog simulation can substitute for that evidence.
